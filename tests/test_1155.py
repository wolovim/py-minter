import pytest


def test_smoke(acct1, acct2, acct3, sbt_1155_contract):
    assert acct1.balance > 0
    assert acct2.balance > 0
    assert acct3.balance > 0
    assert sbt_1155_contract.balanceOf(acct1.address, 1) == 0


def test_contract_owner_can_mint_tokens(acct1, acct2, sbt_1155_contract):
    assert sbt_1155_contract.balanceOf(acct2.address, 1) == 0
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    assert sbt_1155_contract.balanceOf(acct2.address, 1) == 1


def test_owner_cannot_transfer_own_token(acct1, acct2, sbt_1155_contract):
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no transfers"):
        sbt_1155_contract.safeTransferFrom(acct2, acct1, 1, 1, b"", sender=acct2)


def test_contract_owner_cannot_transfer_token(acct1, acct2, sbt_1155_contract):
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    with pytest.raises(Exception, match="Soulbound: no transfers"):
        sbt_1155_contract.safeTransferFrom(acct2, acct1, 1, 1, b"", sender=acct2)


def test_owner_can_mint_to_multiple_receivers(acct1, acct2, acct3, sbt_1155_contract):
    assert sbt_1155_contract.balanceOf(acct1, 1) == 0
    assert sbt_1155_contract.balanceOf(acct2, 1) == 0
    assert sbt_1155_contract.balanceOf(acct3, 1) == 0
    sbt_1155_contract.mintToMany([acct1, acct2, acct3], 1, sender=acct1)
    assert sbt_1155_contract.balanceOf(acct1, 1) == 1
    assert sbt_1155_contract.balanceOf(acct2, 1) == 1
    assert sbt_1155_contract.balanceOf(acct3, 1) == 1


def test_total_supply_increases_on_mintToMany(acct1, acct2, acct3, sbt_1155_contract):
    assert sbt_1155_contract.totalSupply(1) == 0
    sbt_1155_contract.mintToMany([acct1, acct2, acct3], 1, sender=acct1)
    assert sbt_1155_contract.totalSupply(1) == 3


def test_large_many_mint(acct1, acct3, sbt_1155_contract):
    assert sbt_1155_contract.totalSupply(1) == 0
    sbt_1155_contract.mintToMany([acct3] * 300, 1, sender=acct1)
    assert sbt_1155_contract.totalSupply(1) == 300


def test_overly_large_many_mint(acct1, acct3, sbt_1155_contract):
    assert sbt_1155_contract.totalSupply(1) == 0
    with pytest.raises(Exception, match="ran out of gas"):
        sbt_1155_contract.mintToMany([acct3] * 6000, 1, sender=acct1)


def test_get_uri(sbt_1155_contract):
    assert sbt_1155_contract.uri(1) == "http://test.com/{id}.json"


def test_set_uri(acct1, sbt_1155_contract):
    assert sbt_1155_contract.uri(1) == "http://test.com/{id}.json"
    sbt_1155_contract.setURI("http://test2.com/{id}.json", sender=acct1)
    assert sbt_1155_contract.uri(1) == "http://test2.com/{id}.json"


def test_token_owner_cannot_burn_token(acct1, acct2, sbt_1155_contract):
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    assert sbt_1155_contract.balanceOf(acct2, 1) == 1
    with pytest.raises(Exception):
        sbt_1155_contract.burn(acct2.address, 1, 1, sender=acct2)


def test_contract_owner_can_burn_any_token(acct1, acct2, sbt_1155_contract):
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    assert sbt_1155_contract.balanceOf(acct2, 1) == 1
    sbt_1155_contract.burn(acct2.address, 1, 1, sender=acct1)
    assert sbt_1155_contract.balanceOf(acct2, 1) == 0


def test_owner_can_only_have_one_token(acct1, acct2, sbt_1155_contract):
    sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
    assert sbt_1155_contract.balanceOf(acct2, 1) == 1
    with pytest.raises(Exception, match="Soulbound: already minted"):
        sbt_1155_contract.mint(acct2.address, 1, 1, b"", sender=acct1)
