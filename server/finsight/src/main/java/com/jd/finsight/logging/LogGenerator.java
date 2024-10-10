package com.jd.finsight.logging;

public abstract class LogGenerator {
    protected String filePath;
    public AbstractLogger abstractLogger;

    public LogGenerator(String filePath) {
        this.filePath = filePath;
    }

    public abstract void createLogger();

    public void writeLogsToFile(String log) {
        abstractLogger.writeLogsToFile(log);
    }
}
