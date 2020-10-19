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
	
	// getting the equity in Rycoins of an investor
    // working the mapping so it can work within MyEtherWallet
    function equity_rycoins(address investor) external constant returns (uint) {
        return equity_in_rycoins[investor];
    }
    
    // getting the equity in USD of an investor
    // working the mapping so it can work within MyEtherWallet
    function equity_USD(address investor) external constant returns (uint) {
        return equity_in_USD[investor];
    }
	
    // Buying Rycoins
    // external since input variables are not intrinsic to the contract then apply modifier
    // function to get the "Buy Rycoins" action in MyEtherWallet. Will not return anything
    // arguments: address of investor (since investor calls to buy Rycoins)
    //            amount of Rycoins they want to buy with USD
    // modifies/updates three variables: equity_in_USD, equity_in_rycoins, total_rycoins_bought
    function buy_rycoins(address investor, uint USD_invested) external can_buy_rycoins(USD_invested) {
        uint rycoins_bought = USD_invested * USD_to_rycoins;
        equity_in_rycoins[investor] +=  rycoins_bought;
        
        // divide by 1000 to get in USD 
        equity_in_USD[investor] = equity_in_rycoins[investor] / 1000;
        
        // total Rycoins bought by all investors
        total_rycoins_bought += rycoins_bought;
    }

}