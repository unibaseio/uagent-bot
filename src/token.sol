// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Token is ERC20 {
    constructor(string memory symbol, uint256 maxSupply)
        ERC20(symbol, symbol)
    {
      _mint(msg.sender, maxSupply);
    }
}
