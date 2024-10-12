package com.jd.finsight.controllers;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jd.finsight.TestDataUtil;
import com.jd.finsight.domain.HistoricalStockDataEntity;
import com.jd.finsight.services.HistoricalStockDataService;

@SpringBootTest
@ExtendWith(SpringExtension.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
@AutoConfigureMockMvc
public class HistoricalStockDataControllerIntegrationTests {

        private HistoricalStockDataService historicalStockDataService;
        private MockMvc mockMvc;
        private ObjectMapper objMapper;

        @Autowired
        public HistoricalStockDataControllerIntegrationTests(MockMvc mockMvc,
                        HistoricalStockDataService historicalStockDataService) {
                this.mockMvc = mockMvc;
                this.historicalStockDataService = historicalStockDataService;
                this.objMapper = new ObjectMapper();

        }

        @Test
        public void testThatCreateStockSuccessfullyReturnsHttp201Created() throws Exception {
                HistoricalStockDataEntity testHistoricalStockData = TestDataUtil.createTestStockA();
                testHistoricalStockData.setId(null);
                String stockJson = objMapper.writeValueAsString(testHistoricalStockData);

                mockMvc.perform(
                                MockMvcRequestBuilders.post("/stocks")
                                                .contentType(MediaType.APPLICATION_JSON)
                                                .content(stockJson))
                                .andExpect(MockMvcResultMatchers.status().isCreated());
        }

        @Test
        public void testThatCreateStockSuccessfullyReturnsSavedStock() throws Exception {
                HistoricalStockDataEntity testHistoricalStockData = TestDataUtil.createTestStockA();
                testHistoricalStockData.setId(null);
                String stockJson = objMapper.writeValueAsString(testHistoricalStockData);

                // does not test timestamp field
                mockMvc.perform(
                                MockMvcRequestBuilders.post("/stocks")
                                                .contentType(MediaType.APPLICATION_JSON)
                                                .content(stockJson))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.id").isNumber())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.code").value("AMZN"))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.open").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.low").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.high").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.close").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.volume").value(1.0));
        }

        @Test
        public void testThatListStocksReturnsHttpStatus200() throws Exception {
                mockMvc.perform(
                                MockMvcRequestBuilders.get("/stocks")
                                                .contentType(MediaType.APPLICATION_JSON))
                                .andExpect(MockMvcResultMatchers.status().isOk());
        }

        @Test
        public void testThatListStocksReturnsListOfStocks() throws Exception {
                HistoricalStockDataEntity testStockA = TestDataUtil.createTestStockA();
                historicalStockDataService.createStock(testStockA);

                mockMvc.perform(
                                MockMvcRequestBuilders.get("/stocks")
                                                .contentType(MediaType.APPLICATION_JSON))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].id").isNumber())
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].code").value("AMZN"))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].open").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].low").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].high").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].close").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.[0].volume").value(1.0));
                ;
        }

        @Test
        public void testThatListStocksReturnsHttpStatus200WhenStockExists() throws Exception {
                HistoricalStockDataEntity testStockA = TestDataUtil.createTestStockA();
                historicalStockDataService.createStock(testStockA);

                mockMvc.perform(
                                MockMvcRequestBuilders.get("/stocks/1")
                                                .contentType(MediaType.APPLICATION_JSON))
                                .andExpect(MockMvcResultMatchers.status().isOk());
        }

        @Test
        public void testThatListStocksReturnsHttpStatus404WhenNoStockExists() throws Exception {

                mockMvc.perform(
                                MockMvcRequestBuilders.get("/stocks/99")
                                                .contentType(MediaType.APPLICATION_JSON))
                                .andExpect(MockMvcResultMatchers.status().isNotFound());
        }

        @Test
        public void testThatListStocksReturnsStockWhenStockExists() throws Exception {
                HistoricalStockDataEntity testStockA = TestDataUtil.createTestStockA();
                historicalStockDataService.createStock(testStockA);

                mockMvc.perform(
                                MockMvcRequestBuilders.get("/stocks/1")
                                                .contentType(MediaType.APPLICATION_JSON))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value(1))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.code").value("AMZN"))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.open").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.low").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.high").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.close").value(228.957))
                                .andExpect(MockMvcResultMatchers.jsonPath("$.volume").value(1.0));
                ;
        }
}
