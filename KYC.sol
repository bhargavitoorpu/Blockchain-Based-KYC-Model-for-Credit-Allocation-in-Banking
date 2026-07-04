// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract KYC {
    struct Customer {
        string fullName;
        string nationalId;
        string kycStatus;
        string addedByBank;
    }

    mapping(string => Customer) private customers;

    function addCustomer(
        string memory _fullName,
        string memory _nationalId,
        string memory _kycStatus,
        string memory _addedByBank
    ) public {
        customers[_nationalId] = Customer(_fullName, _nationalId, _kycStatus, _addedByBank);
    }

    function getCustomer(string memory _nationalId) public view returns (
        string memory fullName,
        string memory nationalId,
        string memory kycStatus,
        string memory addedByBank
    ) {
        Customer memory c = customers[_nationalId];
        return (c.fullName, c.nationalId, c.kycStatus, c.addedByBank);
    }
}
