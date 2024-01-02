import pytest


def test_smoke(acct1, acct2, acct3, ss_contract):
    assert acct1.balance > 0
    assert acct2.balance > 0
    assert acct3.balance > 0
    assert ss_contract.name() == "Soulbound Token"
    assert ss_contract.symbol() == "SBT"


# def test_set_base_uri(acct1, ss_contract):
#     assert ss_contract.getBaseURI() == ""
#     ss_contract.setBaseURI("http://127.0.0.1:5000", sender=acct1)
#     assert ss_contract.getBaseURI() == "http://127.0.0.1:5000"
#
#
# def test_get_token_uri(acct1, acct2, ss_contract):
#     ss_contract.setBaseURI("http://127.0.0.1:5000", sender=acct1)
#     ss_contract.safeMint(acct2, sender=acct1)
#     assert ss_contract.tokenURI(1) == "http://127.0.0.1:5000/1.json"


def test_contract_owner_can_mint_tokens(acct1, acct2, ss_contract):
    assert ss_contract.balanceOf(acct2) == 0
    ss_contract.safeMint(acct2, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 1


def test_owner_cannot_transfer_own_token(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no transfers"):
        ss_contract.transferFrom(acct2, acct1, 1, sender=acct2)


def test_deployer_cannot_transfer_tokens(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no transfers"):
        ss_contract.transferFrom(acct2, acct1, 1, sender=acct1)


def test_deployer_cannot_safe_transfer_tokens(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no transfers"):
        ss_contract.safeTransferFrom(acct2, acct1, 1, sender=acct1)


def test_token_owner_can_burn_token(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 1
    ss_contract.burn(1, sender=acct2)
    assert ss_contract.balanceOf(acct2) == 0


def test_contract_owner_can_burn_any_token(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 1
    ss_contract.burn(1, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 0


def test_token_id_increments(acct1, acct2, ss_contract):
    assert ss_contract.getNextTokenId() == 1
    ss_contract.safeMint(acct2, sender=acct1)
    ss_contract.safeMint(acct2, sender=acct1)
    ss_contract.safeMint(acct2, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 3
    assert ss_contract.getNextTokenId() == 4


def test_updated_contract_owner_can_burn_any_token(acct1, acct2, acct3, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    ss_contract.transferOwnership(acct3, sender=acct1)
    assert ss_contract.balanceOf(acct2) == 1
    ss_contract.burn(1, sender=acct3)
    assert ss_contract.balanceOf(acct2) == 0


def test_outdated_contract_owner_cannot_burn_any_token(acct1, acct2, acct3, ss_contract):
    ss_contract.safeMint(acct2, sender=acct1)
    ss_contract.transferOwnership(acct3, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no burn except by owner"):
        ss_contract.burn(1, sender=acct1)
        

def test_approve_function_is_prohibited(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct1, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no approvals"):
        ss_contract.approve(acct2, 1, sender=acct1)


def test_approve_all_function_is_prohibited(acct1, acct2, ss_contract):
    ss_contract.safeMint(acct1, sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no approvals"):
        ss_contract.setApprovalForAll(acct2, True, sender=acct1)
