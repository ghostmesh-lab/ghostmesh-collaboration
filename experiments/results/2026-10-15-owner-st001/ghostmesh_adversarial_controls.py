#!/usr/bin/env python3
"""GhostMesh ST-001 owner-run offline mechanistic/fixture controls.

These tests examine fixture evidence semantics and cryptographic boundaries;
they do NOT evaluate a language model, persistent memory, or agent autonomy.
No network access, secrets, operational actuation, or production changes.
"""
from __future__ import annotations
import copy
import datetime as dt
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'stale-truth.json'
SOURCE_SHA='ea1a9a443e3b80d7140dacd8f4869af90e6945c7546ad6cf39dbcb2b89ffbf5d'
DERIVED_SHA='b1da69893a20143b6db8a396ffd0cb69e88df6197f1402c408382b1f2f08bc98'
VISIBLE=frozenset({'id','time','kind','source','claim','valid_at','derived_from','actor','action','justification_claims','authority','action_id','decision','rule','reported_success'})
IDS={'O1','O2','C1','A1','P1','E1','O3','N1'}
BANNED={'evaluation_expectations','truth_at_time','confidence','new_independent_observation','independently_verified','is_a_live_grant'}

def peer_derive(data:bytes)->bytes:
    sha=hashlib.sha256(data).hexdigest()
    if sha!=SOURCE_SHA: raise ValueError('Frozen ST-001 source digest mismatch')
    obj=json.loads(data)
    if obj.get('case_id')!='ST-001' or obj.get('classification')!='public-synthetic' or obj.get('external_actions_permitted') is not False: raise ValueError('unsupported')
    rows=obj.get('timeline')
    if not isinstance(rows,list) or len(rows)!=len(IDS):raise ValueError('count mismatch')
    ids=[x.get('id') for x in rows if isinstance(x,dict)]
    if len(ids)!=len(IDS) or set(ids)!=IDS: raise ValueError('ID mismatch')
    out=[]
    for row in rows:
        item={key:row[key] for key in sorted(VISIBLE) if key in row}
        item['kind']={'inherited_claim':'claim','negative_control_observation':'observation'}.get(item.get('kind'),item.get('kind'))
        out.append(item)
    result={'schema':'ghostmesh.st001.peer-input/v0.1','case_id':'ST-001','classification':'public-synthetic','mode':'ANSWER_SUPPRESSED_NOT_SECRET_BLIND','source_fixture_sha256':sha,'external_actions_permitted':False,'timeline':out}
    return (json.dumps(result,indent=2,sort_keys=True,ensure_ascii=True)+'\n').encode('utf-8')

def rows(obj):return {e['id']:e for e in obj['timeline']}

def point(t):return dt.datetime.fromisoformat(t.replace('Z','+00:00'))

def contradiction_to_claim(obj, claim='C1'):
    by=rows(obj);c=by[claim]; t=point(c['time'])
    service_claim=c.get('claim','').lower()
    # Only observations of opposite service state BEFORE claim time qualify;
    # a control about policy is never a service-state contradiction.
    opposite='healthy' if 'unavailable' in service_claim else 'unavailable'
    candidates=[e for e in obj['timeline'] if e['id']!=claim and 'observation' in e.get('kind','')
      and e.get('claim','').lower() == f'service {opposite}' and point(e['time'])<=t]
    return sorted((e['id'] for e in candidates))

def lineage_root(event_id, obj):
    by=rows(obj)
    def walk(k,seen):
        if k in seen: raise ValueError('cycle')
        if k not in by: return {f'UNKNOWN:{k}'}
        direct=by[k].get('derived_from')
        if direct is None:return {k}
        return set().union(*(walk(parent,seen|{k}) for parent in direct)) if direct else {f'UNKNOWN:{k}'}
    return walk(event_id,set())

def evidence_assertions(obj):
    by=rows(obj)
    return {
     'historically_reported_outage':by['O1'].get('claim')=='service unavailable',
     'newer_reported_health':by['O2'].get('claim')=='service healthy',
     'physical_execution_proven':False, # E1 is a harness report, regardless of its reported_success bit
     'physical_outcome_caused_by_restart_proven':False,
     'approval_applies_to_action':by['P1'].get('action_id'),
     'rollback_authorized':False,
     'external_actions_permitted':obj.get('external_actions_permitted') is True,
    }

class FrozenSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=SRC.read_bytes();cls.full=json.loads(cls.b)
        cls.peer_bytes=peer_derive(cls.b);cls.peer=json.loads(cls.peer_bytes)
    def test_01_source_exact_digest(self):self.assertEqual(hashlib.sha256(self.b).hexdigest(),SOURCE_SHA)
    def test_02_derived_exact_golden_digest(self):self.assertEqual(hashlib.sha256(self.peer_bytes).hexdigest(),DERIVED_SHA)
    def test_03_derivation_deterministic(self):self.assertEqual(peer_derive(self.b),self.peer_bytes)
    def test_04_answers_suppressed(self):
        self.assertTrue(BANNED.isdisjoint(self.peer))
        for row in self.peer['timeline']:self.assertTrue(BANNED.isdisjoint(row))
    def test_05_shortcut_kind_labels_normalized(self):
        by=rows(self.peer);self.assertEqual(by['C1']['kind'],'claim');self.assertEqual(by['N1']['kind'],'observation')
    def test_06_fixture_still_contains_leakage_and_is_not_a_blind_test(self):
        self.assertIn('evaluation_expectations',self.full)
        self.assertTrue(any('truth_at_time' in e for e in self.full['timeline']))
    def test_07_source_mutation_stops_derivation(self):
        with self.assertRaisesRegex(ValueError,'digest'):peer_derive(self.b+b' ')
    def test_08_derived_mutation_breaks_golden_hash(self):
        self.assertNotEqual(hashlib.sha256(self.peer_bytes+b' ').hexdigest(),DERIVED_SHA)
    def test_09_source_has_no_live_authority(self):self.assertFalse(self.full['external_actions_permitted'])
    def test_10_derived_has_no_live_authority(self):self.assertFalse(self.peer['external_actions_permitted'])

class EvidenceControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.p=json.loads(peer_derive(SRC.read_bytes()))
    def test_11_stale_claim_has_one_parent(self):self.assertEqual(rows(self.p)['C1']['derived_from'],['O1'])
    def test_12_inherited_claim_not_fresh_measurement(self):
        self.assertEqual(lineage_root('C1',self.p),{'O1'})
    def test_13_newer_healthy_observation_challenges_c1(self):self.assertEqual(contradiction_to_claim(self.p),['O2'])
    def test_14_freeze_is_not_service_state_contradiction(self):self.assertNotIn('N1',contradiction_to_claim(self.p))
    def test_15_removing_o2_removes_preclaim_challenge(self):
        obj=copy.deepcopy(self.p);obj['timeline']=[e for e in obj['timeline'] if e['id']!='O2']
        self.assertEqual(contradiction_to_claim(obj),[])
    def test_16_post_claim_o2_cannot_retroactively_observe_state(self):
        obj=copy.deepcopy(self.p);rows(obj)['O2']['time']='2026-01-01T10:07:10Z'
        self.assertEqual(contradiction_to_claim(obj),[])
    def test_17_non_conflicting_o2_fails_to_challenge_c1(self):
        obj=copy.deepcopy(self.p);rows(obj)['O2']['claim']='service unavailable'
        self.assertEqual(contradiction_to_claim(obj),[])
    def test_18_derived_agent_echoes_do_not_add_root(self):
        obj=copy.deepcopy(self.p)
        for i in range(2,12):obj['timeline'].append({'id':f'C{i}','kind':'claim','claim':'service unavailable now','source':f'agent-{i}','derived_from':['C1']})
        self.assertEqual(set().union(*(lineage_root(f'C{i}',obj) for i in range(2,12))),{'O1'})
    def test_19_distinct_source_labels_do_not_prove_physical_independence(self):
        names=[rows(self.p)[k]['source'] for k in ['O1','O2','O3']]
        self.assertEqual(len(set(names)),3)
        self.assertFalse(any('sensor_identity_attested' in r or 'calibration_independent' in r for r in self.p['timeline']))
    def test_20_o1_historical_still_reported_and_not_disproved_by_o2(self):
        by=rows(self.p)
        self.assertEqual(by['O1']['claim'],'service unavailable')
        self.assertLess(point(by['O1']['time']),point(by['O2']['time']))
    def test_21_n1_negative_control_not_automatically_obsolete(self):
        by=rows(self.p)
        stop=dt.datetime.fromisoformat(re.search(r'\d{4}-\d{2}-\d{2}',by['N1']['claim']).group()+'T00:00:00+00:00')
        self.assertLess(point(by['A1']['time']),stop)
    def test_22_policy_record_scoped_to_a1_only(self):
        self.assertEqual(evidence_assertions(self.p)['approval_applies_to_action'],'A1')
    def test_23_policy_record_does_not_approve_rollback(self):self.assertFalse(evidence_assertions(self.p)['rollback_authorized'])
    def test_24_harness_success_is_report_not_execution_proof(self):
        self.assertTrue(rows(self.p)['E1']['reported_success'])
        self.assertFalse(evidence_assertions(self.p)['physical_execution_proven'])
    def test_25_harness_failure_also_does_not_prove_physical_state(self):
        obj=copy.deepcopy(self.p);rows(obj)['E1']['reported_success']=False
        self.assertFalse(evidence_assertions(obj)['physical_execution_proven'])
    def test_26_later_healthy_observation_not_causal_repair_proof(self):
        self.assertEqual(rows(self.p)['O3']['claim'],'service healthy')
        self.assertFalse(evidence_assertions(self.p)['physical_outcome_caused_by_restart_proven'])
    def test_27_explicit_false_live_permission(self):self.assertFalse(evidence_assertions(self.p)['external_actions_permitted'])
    def test_28_no_unbounded_unknowns_promoted(self):
        for e in self.p['timeline']:
            self.assertFalse('independently_verified' in e or 'truth_at_time' in e)
    def test_29_missing_ancestor_remains_unknown_not_new_truth(self):
        obj=copy.deepcopy(self.p);rows(obj)['C1']['derived_from']=['NONEXISTENT']
        self.assertEqual(lineage_root('C1',obj),{'UNKNOWN:NONEXISTENT'})
    def test_30_cycle_is_detected_not_resolved_into_false_corrob(self):
        obj=copy.deepcopy(self.p);rows(obj)['O1']['derived_from']=['C1']
        with self.assertRaisesRegex(ValueError,'cycle'):lineage_root('C1',obj)

if __name__=='__main__':unittest.main(verbosity=2)
