package com.jd.finsight.repositories;

import com.jd.finsight.TestDataUtil;
import com.jd.finsight.domain.Stock;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
// included with @SpringBootTest
// @ExtendWith(SpringApplication.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
public class StockRepositoryIntegrationTests {
    private StockRepository underTest;

    // Injects StockRepository Bean into the test when run
    @Autowired
    public StockRepositoryIntegrationTests(StockRepository underTest) {
        this.underTest = underTest;
    }

    @Test
    public void testThatStockCanBeCreatedAndRecalled() {
        Stock stock = TestDataUtil.createTestStockA();
        underTest.save(stock);
        Optional<Stock> result = underTest.findById(stock.getId());
        assertThat(result).isPresent();
        assertThat(result.get()).isEqualTo(stock);
    }
}
