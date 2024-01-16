 // SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "@openzeppelin/token/ERC1155/ERC1155.sol";
import "@openzeppelin/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/access/Ownable.sol";

contract SoulboundToken1155 is ERC1155, ERC1155Burnable, Ownable, ERC1155Supply {
  constructor(address initialOwner) ERC1155("") Ownable(initialOwner) {}

  function mint(address account, uint256 id, uint256 amount, bytes memory data)
    public
    onlyOwner
  {
    _mint(account, id, amount, data);
  }
  
  function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
    public
    onlyOwner
  {
    _mintBatch(to, ids, amounts, data);
  }
  
  // function transferFrom(
  //   address from,
  //   address to,
  //   uint256 id,
  //   uint256 amount
  // ) public override {
  //   require(soulboundOwners[id] == from, "Token is soulbound");
  //   super.transferFrom(from, to, id, amount);
  // }
  function mintToMany(address[] calldata accounts, uint256 id) external onlyOwner {
    require(accounts.length > 0, "No addresses provided");
    
    for (uint256 i = 0; i < accounts.length; i++) {
      _mint(accounts[i], id, 1, "");
    }
  }
  
  // function transferFrom(address from, address to, uint256 tokenId, uint256 amount) public virtual override {
  //   require(from == address(0), "Soulbound: no transfers");
  //   super.transferFrom(from, to, tokenId, amount);
  // }

  // function getNextTokenId() external view returns (uint256) {
  //   return _nextTokenId;
  // }

  // function approve(address to, uint256 tokenId) public override {
  //   revert("Soulbound: no approvals");
  // } 

  function setApprovalForAll(address operator, bool approved) public override {
    revert("Soulbound: no approvals");
  }

  function burn(uint256 id, uint256 amount) external onlyOwner {
    // require(ownerOf(tokenId) == _msgSender() || _msgSender() == owner(), "Soulbound: no burn except by owner");
    // super._burn(tokenId);
    _burn(msg.sender, id, amount);
  }

  // The following functions are overrides required by Solidity.

  function _update(address from, address to, uint256[] memory ids, uint256[] memory values)
      internal
      override(ERC1155, ERC1155Supply)
  {
      super._update(from, to, ids, values);
  }
}
