package com.jd.finsight.logging.impl;

import java.io.IOException;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

import com.jd.finsight.logging.LogFactory;

public class GenericLogFactory extends LogFactory {

    public GenericLogFactory(String filePath) {
        super(filePath);
    }

    @Override
    public void writeLogsToFile(String log) {
        Logger logger = Logger.getLogger("GenericLogFactoryLogger");
        FileHandler fh;

        try {

            // This block configures the logger with handler and formatter
            // true param for file handler enables append mode
            fh = new FileHandler(filePath, true);
            logger.addHandler(fh);

            SimpleFormatter formatter = new SimpleFormatter();
            fh.setFormatter(formatter);

            logger.info(log);

            fh.close();
        } catch (SecurityException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
