 // SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "@openzeppelin/token/ERC721/ERC721.sol";
import "@openzeppelin/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/access/Ownable.sol";

contract SoulboundToken is ERC721, ERC721Burnable, Ownable {
  uint256 private _nextTokenId = 1;

  constructor(string memory name, string memory symbol, address initialOwner)
    ERC721(name, symbol)
    Ownable(initialOwner)
  {}

  function safeMint(address to) external onlyOwner {
    _safeMint(to, _nextTokenId);
    _nextTokenId++;
  }

  function transferFrom(address from, address to, uint256 tokenId) public virtual override {
    require(from == address(0), "Soulbound: no transfers");
  }

  function getNextTokenId() external view returns (uint256) {
    return _nextTokenId;
  }

  function approve(address to, uint256 tokenId) public override {
    revert("Soulbound: no approvals");
  } 

  function setApprovalForAll(address operator, bool approved) public override {
    revert("Soulbound: no approvals");
  }

  function burn(uint256 tokenId) public virtual override {
    require(ownerOf(tokenId) == _msgSender() || _msgSender() == owner(), "Soulbound: no burn except by owner");
    super._burn(tokenId);
  }


  // function _update(address to, uint256 tokenId, address auth) internal virtual override returns (address) {
    // require(ownerOf(tokenId) == auth || auth == owner(), "Only the contract owner or owner of the token can burn it.");
    // require(to == address(0), "SOULBOUND!");
    // super._update(to, tokenId, auth);
  // }
}
