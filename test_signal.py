import math

def get_signal(mNav, regime, trend, blackout=False, ownershipCtx=None, absorptionCtx=None, btcPerShareTrend=None):
    """
    Replicates the getSignal logic from mstr-signal-engine.html.
    Returns a dict with keys: key, label, reason, blackout and possibly contexts.
    """
    # Definition of signal prototypes
    SIG = {
        'NEUT': {'key': 'NEUT', 'label': 'Neutral / Avoid'},
        'CAUT': {'key': 'CAUT', 'label': 'Caution'},
        'LONG': {'key': 'LONG', 'label': 'Long MSTR'},
        'HOLD': {'key': 'HOLD', 'label': 'Hold / Monitor'},
        'REDUCE': {'key': 'REDUCE', 'label': 'Reduce / Hedge'},
        'SHORT': {'key': 'SHORT', 'label': 'Short MSTR / Long BTC'},
        'BTCOV': {'key': 'BTCOV', 'label': 'Hold BTC, avoid MSTR'},
    }

    # Factor 3: BTC trend override
    if trend == 'downtrend':
        return {
            **SIG['NEUT'],
            'reason': 'BTC in downtrend — avoid MSTR regardless of mNAV or ATM regime',
            'blackout': blackout,
            'ownershipCtx': ownershipCtx,
        }

    # Pending regime override
    if regime == 'Pending':
        return {
            **SIG['CAUT'],
            'reason': 'ATM proceeds not yet deployed — reported metrics understated. Do not trade.',
            'blackout': blackout,
            'ownershipCtx': ownershipCtx,
        }

    # Factor 1 + Factor 2: valuation + issuance
    base = None
    if mNav < 1.00 and regime in ('Dormant', 'Light'):
        base = {
            **SIG['LONG'],
            'reason': f"{((1 - mNav) * 100):.1f}% discount to NAV · ATM {regime.lower()} · favorable entry"
        }
    elif mNav < 1.00 and regime == 'Active':
        base = {
            **SIG['HOLD'],
            'reason': 'Discount to NAV but ATM supply active — upside capped. Wait for Dormant.'
        }
    elif mNav < 1.10:
        base = {
            **SIG['HOLD'],
            'reason': 'At fair value with active ATM — premium ceiling forming. Do not chase.' if regime in ('Active', 'Aggressive')
                     else 'Near fair value, ATM manageable — hold if BTC trend constructive.'
        }
    elif mNav < 1.20:
        base = {
            **SIG['REDUCE'],
            'reason': f"mNAV {mNav:.2f}× · ATM {regime.lower()} · company likely selling into this premium."
        }
    else:
        base = {
            **SIG['SHORT'],
            'reason': f"mNAV {mNav:.2f}× + {regime} ATM — systematic seller above fair value. Equal-dollar pair."
        }

    # Ownership modifier
    if ownershipCtx:
        sig = ownershipCtx.get('signal')
        if sig == 'btc_over_mstr' and base['key'] in ('LONG', 'HOLD'):
            return {
                **SIG['BTCOV'],
                'reason': 'Ownership expanding but BTC/share accretion weak — equity supply pressure dominates. Hold BTC; reduce MSTR exposure.',
                'blackout': blackout,
                'ownershipCtx': ownershipCtx,
            }
        if sig == 'bullish' and base['key'] == 'LONG':
            base = {
                **base,
                'reason': base['reason'] + ' · Ownership factor confirms: rising BTC% + accretive ATM.'
            }
        if sig == 'risk_off':
            return {
                **SIG['REDUCE'],
                'reason': 'MSTR BTC holdings declining — forced-sale or capital deployment halt risk. Reduce exposure.',
                'blackout': blackout,
                'ownershipCtx': ownershipCtx,
            }

    # Absorption modifier
    if absorptionCtx and absorptionCtx.get('ratio') is not None:
        ratio = absorptionCtx['ratio']
        if ratio >= 0.15 and base['key'] in ('LONG', 'HOLD'):
            return {
                **SIG['HOLD'],
                'reason': f'ATM supply critical — daily issuance is {int(round(ratio * 100))}% of avg volume. Market absorbing under pressure. Do not chase.',
                'blackout': blackout,
                'ownershipCtx': ownershipCtx,
                'absorptionCtx': absorptionCtx,
                'btcPerShareTrend': btcPerShareTrend,
            }

    # BTC/share trend modifier
    if btcPerShareTrend and btcPerShareTrend.get('trend') == 'falling' and base['key'] == 'LONG':
        return {
            **SIG['HOLD'],
            'reason': 'BTC/share declining despite purchases — dilution outpacing accumulation. Wait for BTC/share trend to reverse.',
            'blackout': blackout,
            'ownershipCtx': ownershipCtx,
            'absorptionCtx': absorptionCtx,
            'btcPerShareTrend': btcPerShareTrend,
        }

    # Base case
    return {**base, 'blackout': blackout, 'ownershipCtx': ownershipCtx, 'absorptionCtx': absorptionCtx, 'btcPerShareTrend': btcPerShareTrend}


def test_cases():
    """Runs a set of assertions for core scenarios."""
    def assert_signal(case_id, result, expected_key):
        assert result['key'] == expected_key, f"Case {case_id}: expected {expected_key}, got {result['key']} (reason: {result['reason']})"

    # 1. mNAV 0.95, Dormant, uptrend → LONG
    result1 = get_signal(0.95, 'Dormant', 'uptrend')
    assert_signal('1', result1, 'LONG')

    # 2. mNAV 0.95, Active, uptrend → HOLD (discount but active ATM)
    result2 = get_signal(0.95, 'Active', 'uptrend')
    assert_signal('2', result2, 'HOLD')

    # 3. mNAV 1.05, Aggressive, range → HOLD according to current logic
    result3 = get_signal(1.05, 'Aggressive', 'range')
    assert_signal('3', result3, 'HOLD')

    # 4. mNAV 1.30, Aggressive, uptrend → SHORT
    result4 = get_signal(1.30, 'Aggressive', 'uptrend')
    assert_signal('4', result4, 'SHORT')

    # 5. Downtrend overrides everything
    result5 = get_signal(0.90, 'Dormant', 'downtrend')
    assert_signal('5', result5, 'NEUT')

    # 6. Pending regime returns CAUT
    result6 = get_signal(0.90, 'Pending', 'uptrend')
    assert_signal('6', result6, 'CAUT')

    # 7. Ownership: btc_over_mstr downgrades LONG/HOLD to BTCOV
    result7 = get_signal(0.95, 'Dormant', 'uptrend', ownershipCtx={'signal': 'btc_over_mstr'})
    assert_signal('7', result7, 'BTCOV')

    # 8. Ownership: risk_off returns REDUCE regardless
    result8 = get_signal(0.95, 'Dormant', 'uptrend', ownershipCtx={'signal': 'risk_off'})
    assert_signal('8', result8, 'REDUCE')

    # 9. Absorption ratio critical downgrades LONG/HOLD to HOLD
    result9 = get_signal(0.95, 'Dormant', 'uptrend', absorptionCtx={'ratio': 0.18})
    assert_signal('9', result9, 'HOLD')

    # 10. BTC/share falling downgrades LONG to HOLD
    result10 = get_signal(0.95, 'Dormant', 'uptrend', btcPerShareTrend={'trend': 'falling'})
    assert_signal('10', result10, 'HOLD')

    print("All test cases passed.")


if __name__ == '__main__':
    test_cases()
