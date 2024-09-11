package com.jd.finsight;

import lombok.extern.java.Log;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.sql.DataSource;

@SpringBootApplication
@Log
public class FinsightApplication implements CommandLineRunner {

	private final DataSource dataSource;

	//constructor
	public FinsightApplication(final DataSource dataSource) {
		this.dataSource = dataSource;
	}

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

		log.info("Datasource: " + dataSource.toString());
		final JdbcTemplate restTemplate = new JdbcTemplate(dataSource);
		restTemplate.execute("select 1");
	}

	public void appMethod() throws Exception {
		int i = 0;

		System.out.println(i++);
		Thread.sleep(1000);
		System.out.println(i++);
	}
}