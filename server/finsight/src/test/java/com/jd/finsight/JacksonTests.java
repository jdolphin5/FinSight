package com.jd.finsight;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jd.finsight.domain.Stock;
import com.jd.finsight.repositories.StockRepository;

@SpringBootTest
@ExtendWith(SpringExtension.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
public class JacksonTests {

    private ObjectMapper objMapper;

    @Autowired
    public JacksonTests(final ObjectMapper objMapper) {
        this.objMapper = objMapper;
    }

    @Test
    public void testThatObjectMapperCanCreateJsonFromJavaObject() throws JsonProcessingException {
        Stock stock = TestDataUtil.createTestStockA();

        String res = objMapper.writeValueAsString(stock);
        assertThat(res).isEqualTo(
                "{\"id\":1,\"code\":\"AMZN\",\"local_time\":\"2024-09-01T14:00:00.000+00:00\",\"open\":228.957,\"high\":228.957,\"low\":228.957,\"close\":228.957,\"volume\":1.0}");
    }

    @Test
    public void testThatObjectMapperCanCreateJavaObjectFromJsonObject() throws JsonProcessingException {
        String json = "{\"id\":1,\"code\":\"AMZN\",\"local_time\":\"2024-09-01T14:00:00.000+00:00\",\"open\":228.957,\"high\":228.957,\"low\":228.957,\"close\":228.957,\"volume\":1.0}";

        Stock stock = objMapper.readValue(json, Stock.class);
        assertThat(stock).isEqualTo(TestDataUtil.createTestStockA());
    }
}
