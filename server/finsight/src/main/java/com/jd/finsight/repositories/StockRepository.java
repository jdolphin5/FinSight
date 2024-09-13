package com.jd.finsight.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.jd.finsight.domain.Stock;

@Repository
public interface StockRepository extends CrudRepository<Stock, Long> {
}