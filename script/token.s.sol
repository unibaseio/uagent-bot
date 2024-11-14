// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "../src/token.sol";
import {Script, console2} from "forge-std/Script.sol";
contract SpaceScript is Script {
    uint256 secret;
    function setUp() public {
        secret = vm.envUint("SECRET");
    }

    function deploy() public {
        vm.startBroadcast(secret);
        vm.stopBroadcast();
    }
}
