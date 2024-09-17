package com.jd.finsight.repositories;

import com.jd.finsight.TestDataUtil;
import com.jd.finsight.domain.HistoricalStockData;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
// included with @SpringBootTest
@ExtendWith(SpringExtension.class)
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
public class HistoricalStockDataRepositoryIntegrationTests {
    private HistoricalStockDataRepository underTest;

    // Injects StockRepository Bean into the test when run
    @Autowired
    public HistoricalStockDataRepositoryIntegrationTests(HistoricalStockDataRepository underTest) {
        this.underTest = underTest;
    }

    @Test
    public void testThatStockCanBeCreatedAndRecalled() {
        HistoricalStockData stock = TestDataUtil.createTestStockA();
        underTest.save(stock);
        Optional<HistoricalStockData> result = underTest.findById(stock.getId());
        assertThat(result).isPresent();
        assertThat(result.get()).isEqualTo(stock);
    }

    @Test
    public void testThatMultipleStocksCanBeCreatedAndRecalled() {
        HistoricalStockData stockA = TestDataUtil.createTestStockA();
        underTest.save(stockA);

        HistoricalStockData stockB = TestDataUtil.createTestStockB();
        underTest.save(stockB);

        HistoricalStockData stockC = TestDataUtil.createTestStockC();
        underTest.save(stockC);

        Iterable<HistoricalStockData> result = underTest.findAll();
        assertThat(result)
                .hasSize(3)
                .containsExactly(stockA, stockB, stockC);
    }

    @Test
    public void testThatStockCanBeUpdated() {
        HistoricalStockData stockA = TestDataUtil.createTestStockA();
        underTest.save(stockA);

        stockA.setCode("NVDA");
        underTest.save(stockA);

        Optional<HistoricalStockData> result = underTest.findById(stockA.getId());
        assertThat(result).isPresent();
        assertThat(result.get()).isEqualTo(stockA);
    }

    @Test
    public void testThatStockCanBeDeleted() {
        HistoricalStockData stockA = TestDataUtil.createTestStockA();
        underTest.save(stockA);
        underTest.deleteById(stockA.getId());
        Optional<HistoricalStockData> result = underTest.findById(stockA.getId());
        assertThat(result).isEmpty();
    }
}