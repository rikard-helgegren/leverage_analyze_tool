/**
 * Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
 *
 * This software is only allowed for private use. As a private user you are allowed to copy,
 * modify, use, and compile the software. You are NOT however allowed to publish, sell, or
 * distribute this software, either in source code form or as a compiled binary, for any purpose,
 * commercial or non-commercial, by any means.
 */

#include <iostream>
#include <vector>

//#pragma once

#define CATCH_CONFIG_MAIN
#include "../../catch.hpp"
#include "../../../src/model/histogram/utils.cpp"
#include "../helpers/ParametersBuilder.cpp"

/** Not prioratized now
TEST_CASE( "Test mapIndexNrToMarketNr function", "[mapIndexNrToMarketNr]" ) {


  REQUIRE(1 == 0);

}*/


TEST_CASE( "Test setStartValuesOfInstruments function", "[setStartValuesOfInstruments]" ) {

    Parameters parameters = Parameters_builder()
            .set_nrOfInstruments(1)
            .set_proportionFunds(1.0f)
            .set_proportionLeverage(0.0f)
            .set_numberOfFunds(1)
            .set_numberOfLeveragedInstruments(0)
            .build();
    const int arraySize = 2;  // Change size according needs
    float currentValues[arraySize] = {-1.0, -1.0};

    setStartValuesOfInstruments(parameters, currentValues);
    REQUIRE(currentValues[0] == 1);

    parameters = Parameters_builder()
            .set_nrOfInstruments(2)
            .set_proportionFunds(0.5f)
            .set_proportionLeverage(0.5f)
            .set_numberOfFunds(1)
            .set_numberOfLeveragedInstruments(1)
            .build();

    setStartValuesOfInstruments(parameters, currentValues);
    REQUIRE(currentValues[0] == 0.5f);

    
    parameters = Parameters_builder()
            .set_nrOfInstruments(2)
            .set_proportionFunds(0.5f)
            .set_proportionLeverage(0.5f)
            .set_numberOfFunds(1)
            .set_numberOfLeveragedInstruments(1)
            .build();

    setStartValuesOfInstruments(parameters, currentValues);
    REQUIRE(currentValues[0] == 0.5f);

}


TEST_CASE( "Test updateCurrentInstrumentValue function", "[updateCurrentInstrumentValue]" ) {

    // update a increase

    float** floatPtrMarektDailyChange = new float*[1];
    floatPtrMarektDailyChange[0] = new float[1];
    floatPtrMarektDailyChange[0][0] = 1.0f;

    Parameters parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,1})
            .set_marketDailyChanges(floatPtrMarektDailyChange)
            .set_includeFeeStatus(false)
            .build();
    float* currentValues = new float[3]{1.0f};
    int item = 0;
    int day = 0;

    float returnData = updateCurrentInstrumentValue(parameters, currentValues, item, day);
    float expectedData = 2;

    REQUIRE(returnData == expectedData);

    floatPtrMarektDailyChange[0][0] = 0.5f;

    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,1})
            .set_marketDailyChanges(floatPtrMarektDailyChange)
            .set_includeFeeStatus(false)
            .build();
        currentValues = new float[3]{1.0f};
        item = 0;
        day = 0;

        returnData = updateCurrentInstrumentValue(parameters, currentValues, item, day);
        expectedData = 1.5;

        REQUIRE(returnData == expectedData);

    // update a decrease
    floatPtrMarektDailyChange[0][0] = -0.5f;

    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,1})
            .set_marketDailyChanges(floatPtrMarektDailyChange)
            .set_includeFeeStatus(false)
            .build();
        currentValues = new float[3]{1.0f};
        item = 0;
        day = 0;

        returnData = updateCurrentInstrumentValue(parameters, currentValues, item, day);
        expectedData = 0.5;

        REQUIRE(returnData == expectedData);

     floatPtrMarektDailyChange[0][0] = -1.0f;

    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,1})
            .set_marketDailyChanges(floatPtrMarektDailyChange)
            .set_includeFeeStatus(false)
            .build();
    currentValues = new float[3]{1.0f};
    item = 0;
    day = 0;

    returnData = updateCurrentInstrumentValue(parameters, currentValues, item, day);
    expectedData = 0.0f;

    REQUIRE(returnData == expectedData);
}



TEST_CASE( "Test checkPreConditionsRebalanceTime function", "[checkPreConditionsRebalanceTime]" ) {

    //input fund return false
    Parameters parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,2})
            .set_numberOfFunds(1)
            .build();
    int item = 0;
    int day = 6;

    bool returnData = checkPreConditionsRebalanceTime(parameters, day, item);
    bool expectedData = false;

    REQUIRE(returnData == expectedData);

    //no fund to rebalance return false
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2})
            .set_numberOfFunds(0)
            .build();
    item = 0;
    day = 6;

    returnData = checkPreConditionsRebalanceTime(parameters, day, item);
    expectedData = false;

    REQUIRE(returnData == expectedData);

    //day not 6 mont return false
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .build();
    item = 0;
    day = 5;

    returnData = checkPreConditionsRebalanceTime(parameters, day, item);
    expectedData = false;

    REQUIRE(returnData == expectedData);

    //day is 0 return false
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .build();
    item = 0;
    day = 0;

    returnData = checkPreConditionsRebalanceTime(parameters, day, item);
    expectedData = false;

    REQUIRE(returnData == expectedData);

    //all passed return true
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .build();
    item = 0;
    day = 6;

    returnData = checkPreConditionsRebalanceTime(parameters, day, item);
    expectedData = true;

    REQUIRE(returnData == expectedData);

}

TEST_CASE("Test checkPreConditionsHarvestRefill function","[checkPreConditionsHarvestRefill]"){

    //input fund return false
    Parameters parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{1,2})
            .set_numberOfFunds(1)
            .set_harvestPoint(1.5f)
            .set_refillPoint(0.5f)
            .build();

    float* referenceValue = new float[3]{1.0f};
    float* currentValues = new float[3]{2.0f};
    int item = 0;

    bool returnData = checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues, item);
    bool expectedData = false;

    REQUIRE(returnData==expectedData);

    //No funds return false
    parameters = Parameters_builder()
                .set_instrumentLeverages(new int[20]{2})
                .set_numberOfFunds(0)
                .set_harvestPoint(1.5f)
                .set_refillPoint(0.5f)
                .build();

    referenceValue = new float[3]{1.0f};
    currentValues = new float[3]{2.0f};
    item = 0;

    returnData = checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues, item);
    expectedData = false;

    REQUIRE(returnData==expectedData);

    //current is close to refrence, no rebalance return false
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .set_harvestPoint(1.5f)
            .set_refillPoint(0.5f)
            .build();

    referenceValue = new float[3]{1.0f};
    currentValues = new float[3]{1.1f};
    item = 0;

    returnData = checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues, item);
    expectedData = false;

    REQUIRE(returnData==expectedData);

     //All fullfilled, refrence low return true
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .set_harvestPoint(1.5f)
            .set_refillPoint(0.5f)
            .build();

    referenceValue = new float[3]{1.0f};
    currentValues = new float[3]{0.2f};
    item = 0;

    returnData = checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues, item);
    expectedData = true;

    REQUIRE(returnData==expectedData);

    //All fullfilled return true
    parameters = Parameters_builder()
            .set_instrumentLeverages(new int[20]{2,1})
            .set_numberOfFunds(1)
            .set_harvestPoint(1.5f)
            .set_refillPoint(0.5f)
            .build();

    referenceValue = new float[3]{1.0f};
    currentValues = new float[3]{2.0f};
    item = 0;

    returnData = checkPreConditionsHarvestRefill(parameters, referenceValue, currentValues, item);
    expectedData = true;

    REQUIRE(returnData==expectedData);

}



TEST_CASE( "Test doRebalancing function", "[doRebalancing]" ) {

    //Leverage high rebalance
    Parameters parameters = Parameters_builder()
        .set_instrumentLeverages(new int[20]{2,1})
        .set_numberOfFunds(1)
        .set_nrOfInstruments(2)
        .build();

    float totForRebalancing = 2.0f;
    float* referenceValue = new float[3]{1.0f, 1.0f};
    float* currentValues = new float[3]{2.0f, 0.0f};
    int item = 0;

   doRebalancing(parameters, totForRebalancing, referenceValue, currentValues, item);

   float* expectedData = new float[3]{1.0f, 1.0f};;

   REQUIRE(currentValues[0] == expectedData[0]);
   REQUIRE(currentValues[1] == expectedData[1]);


   //funds high rebalance
   parameters = Parameters_builder()
       .set_instrumentLeverages(new int[20]{2,1})
       .set_numberOfFunds(1)
       .set_nrOfInstruments(2)
       .build();

   totForRebalancing = 2.0f;
   referenceValue = new float[3]{1.0f, 1.0f};
   currentValues = new float[3]{0.0f, 2.0f};
   item = 0;

  doRebalancing(parameters, totForRebalancing, referenceValue, currentValues, item);

  expectedData = new float[3]{1.0f, 1.0f};;

  REQUIRE(currentValues[0] == expectedData[0]);
  REQUIRE(currentValues[1] == expectedData[1]);

  //not enough for rebalance
     parameters = Parameters_builder()
         .set_instrumentLeverages(new int[20]{2,1})
         .set_numberOfFunds(1)
         .set_nrOfInstruments(2)
         .build();

     totForRebalancing = 0.3f;
     referenceValue = new float[3]{1.0f, 1.0f};
     currentValues = new float[3]{0.3f, 0.1f};
     item = 0;

    doRebalancing(parameters, totForRebalancing, referenceValue, currentValues, item);

    expectedData = new float[3]{0.3f, 0.1f};;

    REQUIRE(currentValues[0] == expectedData[0]);
    REQUIRE(currentValues[1] == expectedData[1]);

}
