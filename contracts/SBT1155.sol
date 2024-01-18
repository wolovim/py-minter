 // SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "@openzeppelin/token/ERC1155/ERC1155.sol";
import "@openzeppelin/token/ERC1155/extensions/ERC1155Burnable.sol";
import "@openzeppelin/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/access/Ownable.sol";

contract SoulboundToken1155 is ERC1155, ERC1155Burnable, Ownable, ERC1155Supply {
  constructor(address initialOwner, string memory uri) ERC1155(uri) Ownable(initialOwner) {}

   function setURI(string memory newuri) public onlyOwner {
     _setURI(newuri);
   }

  function mint(address account, uint256 id, uint256 amount, bytes memory data)
    public
    onlyOwner
  {
    require(balanceOf(account, id) == 0, "Soulbound: already minted");
    _mint(account, id, amount, data);
  }
  
  function mintBatch(address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data)
    public
    onlyOwner
  {
    _mintBatch(to, ids, amounts, data);
  }
  
  function mintToMany(address[] calldata accounts, uint256 id) external onlyOwner {
    require(accounts.length > 0, "No addresses provided");
    
    for (uint256 i = 0; i < accounts.length; i++) {
      _mint(accounts[i], id, 1, "");
    }
  }

  function safeTransferFrom(
    address from,
    address to,
    uint256 id,
    uint256 amount,
    bytes memory data
  ) public override {
    require(true == false, "Soulbound: no transfers");
  }

  function setApprovalForAll(address operator, bool approved) public override {
    revert("Soulbound: no approvals");
  }

  function burn(address account, uint256 id, uint256 value) public virtual onlyOwner override {
    _burn(account, id, 1);
  }

  // The following functions are overrides required by Solidity.

  function _update(address from, address to, uint256[] memory ids, uint256[] memory values)
      internal
      override(ERC1155, ERC1155Supply)
  {
      super._update(from, to, ids, values);
  }
}
