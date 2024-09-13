package com.jd.finsight;

//import lombok.extern.java.Log;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
// @Log
public class FinsightApplication implements CommandLineRunner {

	/*
	 * 
	 * private final JdbcTemplate jdbcTemplate;
	 * 
	 * //constructor
	 * public FinsightApplication(final JdbcTemplate jdbcTemplate) {
	 * this.jdbcTemplate = jdbcTemplate;
	 * }
	 * 
	 */

	public static void main(String[] args) {
		SpringApplication.run(FinsightApplication.class, args);
	}

	@Override
	public void run(final String... args) {
		try {
			appMethod();
		} catch (Exception e) {
			System.out.println(e.toString());
		}

		// DataInserter dataInserter = new DataInserter(jdbcTemplate);
		// dataInserter.loadCsvData(jdbcTemplate);
		// jdbcTemplate.execute("SELECT 1");
	}

	public void appMethod() throws Exception {
		int i = 0;

		System.out.println(i++);
		// Thread.sleep(1000);
		// System.out.println(i++);
	}
}