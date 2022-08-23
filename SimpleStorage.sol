// SPDX-License-Identifier: MIT

pragma solidity >= 0.6.0 < 0.9.0;

contract SimpleStorage {

    uint256 Salary;

    // This is a comment!
    struct Employees {
        uint256 Salary;
        string name;
    }

    Employees[] public employee;
    mapping(string => uint256) public nameToSalary;

    function store(uint256 _Salary) public {
        Salary = _Salary;
    }
    
    function retrieve() public view returns (uint256){
        return Salary;
    }

    function addPerson(string memory _name, uint256 _Salary) public {
        employee.push(Employees(_Salary, _name));
        nameToSalary[_name] = _Salary;
    }
}