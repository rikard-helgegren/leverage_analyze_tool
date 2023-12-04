/**
 * Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */


#pragma once
#include <string>
#include "../../../src/model/histogram/Parameters.cpp"


class Parameters_builder{

    private:
        Parameters parameters;

    public:

    Parameters_builder(){
        this->parameters.loan = 0.0f;

        this->parameters.instrumentLeverages = new int[20]{1,1};

        this->parameters.nrOfInstruments = 1;
        this->parameters.instrumentNames = {"OMX30"};
        this->parameters.proportionFunds = 1.0f;
        this->parameters.proportionLeverage = 0.0f;
        this->parameters.totNrDays = 2;
        this->parameters.nrMarketsSelected = 1;


        float** floatPtrMarektDailyChange = new float*[2];

        // Create the first inner list and set its element to 1
        floatPtrMarektDailyChange[0] = new float[1];
        floatPtrMarektDailyChange[0][0] = 1.0f;

        // Create the second inner list and set its element to 1
        floatPtrMarektDailyChange[1] = new float[1];
        floatPtrMarektDailyChange[1][0] = 1.0f;

        this->parameters.marketDailyChanges = floatPtrMarektDailyChange;

        /*
        this->parameters.marketDailyChanges = new float[4][5]{{1.0f,1.0f},
                                                              {1.0f,1.0f},
                                                              {1.0f,1.0f}};


        std::vector<std::vector<float>> vveeccttoorr = {{1.0f,1.0f},
                                                        {1.0f,1.0f},
                                                        {1.0f,1.0f}};
        */


        this->parameters.indexNames = {"OMX30"};
        this->parameters.daysInvesting = 3;
        this->parameters.harvestPoint = 1.5f;
        this->parameters.refillPoint = 0.5f;
        this->parameters.rebalance_period_months = 6;
        this->parameters.strategy = 0;
        this->parameters.volatilityStrategieSampleSize = 0;  //TODO Not to be used yet
        this->parameters.varianceCalcSampleSize = 0;  //TODO Not to be used yet
        this->parameters.volatilityStrategieLevel = 0.0f;   //TODO Not to be used yet
        //this->parameters.outData = new float;
        this->parameters.numberOfLeveragedInstruments = 0;
        this->parameters.numberOfFunds = 1;
        this->parameters.includeFeeStatus = false;
        this->parameters.indexToMarket =  {{1, 1}};

    }



    Parameters build(){
        return this->parameters;
    }

    Parameters_builder set_loan(float loan){
        this->parameters.loan = loan;
        return *this;
    }

    Parameters_builder set_instrumentLeverages(int* instrumentLeverages){
        this->parameters.instrumentLeverages = instrumentLeverages;
        return *this;
    }

    Parameters_builder set_nrOfInstruments(int nrOfInstruments){
        this->parameters.nrOfInstruments = nrOfInstruments;
        return *this;
    }

    Parameters_builder set_instrumentNames(std::vector<std::string> instrumentNames){
        this->parameters.instrumentNames = instrumentNames;
        return *this;
    }

    Parameters_builder set_proportionFunds(float proportionFunds){
        this->parameters.proportionFunds = proportionFunds;
        return *this;
    }

    Parameters_builder set_proportionLeverage(float proportionLeverage){
        this->parameters.proportionLeverage = proportionLeverage;
        return *this;
    }

    Parameters_builder set_totNrDays(int totNrDays){
        this->parameters.totNrDays = totNrDays;
        return *this;
    }

    Parameters_builder set_nrMarketsSelected(int nrMarketsSelected){
        this->parameters.nrMarketsSelected = nrMarketsSelected;
        return *this;
    }

    Parameters_builder set_marketDailyChanges(float** marketDailyChanges){
        this->parameters.marketDailyChanges = marketDailyChanges;
        return *this;
    }

    Parameters_builder set_indexNames(std::vector<std::string> indexNames){
        this->parameters.indexNames = indexNames;
        return *this;
    }

    Parameters_builder set_daysInvesting(int daysInvesting){
        this->parameters.daysInvesting = daysInvesting;
        return *this;
    }

    Parameters_builder set_harvestPoint(float harvestPoint){
        this->parameters.harvestPoint = harvestPoint;
        return *this;
    }

    Parameters_builder set_refillPoint(float refillPoint){
        this->parameters.refillPoint = refillPoint;
        return *this;
    }

    Parameters_builder set_rebalance_period_months(int rebalance_period_months){
        this->parameters.rebalance_period_months = rebalance_period_months;
        return *this;
    }

    Parameters_builder set_strategy(int strategy){
        this->parameters.strategy = strategy;
        return *this;
    }

    Parameters_builder set_volatilityStrategieSampleSize(int volatilityStrategieSampleSize){
        this->parameters.volatilityStrategieSampleSize = volatilityStrategieSampleSize;
        return *this;
    }

    Parameters_builder set_varianceCalcSampleSize(int varianceCalcSampleSize){
        this->parameters.varianceCalcSampleSize = varianceCalcSampleSize;
        return *this;
    }

    Parameters_builder set_volatilityStrategieLevel(float volatilityStrategieLevel){
        this->parameters.volatilityStrategieLevel = volatilityStrategieLevel;
        return *this;
    }

    Parameters_builder set_outData(float* outData){
        this->parameters.outData = outData;
        return *this;
    }

    Parameters_builder set_numberOfLeveragedInstruments(int numberOfLeveragedInstruments){
        this->parameters.numberOfLeveragedInstruments = numberOfLeveragedInstruments;
        return *this;
    }

    Parameters_builder set_numberOfFunds(int numberOfFunds){
        this->parameters.numberOfFunds = numberOfFunds;
        return *this;
    }

    Parameters_builder set_includeFeeStatus(bool includeFeeStatus){
        this->parameters.includeFeeStatus = includeFeeStatus;
        return *this;
    }


    Parameters_builder set_indexToMarket(std::map<int, int> indexToMarket){
        this->parameters.indexToMarket = indexToMarket;
        return *this;
    }
};
