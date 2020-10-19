//  Rycoins ICO

// Version of compiler
pragma solidity >=0.4.22 <0.7.0;

contract rycoin_ico {
    
    // introducing the maximum number of Rycoins available for sale (1 million for example)
    unint public max_rycoins = 1000000;
    
    // introducing the USD to Rycoins conversion rate (assuming $1 USD = 1000 Rycoins)
    uint public USD_to_rycoins = 1000;
    
    // introducing the total number of Rycoins that have been bought by investors
    uint public total_rycoins_bought = 0;
    
    // mapping from the investor address to its equity in Rycoins and USD 
    mapping(address => uint) equity_in_rycoins;
    mapping(address => uint) equity_in_USD;
    
    // checking if an investor can buy Rycoins
    // _; means that will only be satisfied if the modifier holds true
    modifier can_buy_rycoins(uint USD_invested) {
        require (USD_invested * USD_to_rycoins + total_rycoins_bought <= max_rycoins);
        _;
    }

}