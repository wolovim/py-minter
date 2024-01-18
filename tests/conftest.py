import pytest


@pytest.fixture
def acct1(accounts):
    return accounts[0]


@pytest.fixture
def acct2(accounts):
    return accounts[1]


@pytest.fixture
def acct3(accounts):
    return accounts[2]


@pytest.fixture
def ss_contract(acct1, project):
    return acct1.deploy(project.SoulboundToken, "Soulbound Token", "SBT", acct1.address)


@pytest.fixture
def sbt_1155_contract(acct1, project):
    return acct1.deploy(
        project.SoulboundToken1155, acct1.address, "http://test.com/{id}.json"
    )
