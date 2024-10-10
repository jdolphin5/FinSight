package com.jd.finsight.command;

public class LogCommand extends Command {
    private String log;
    private String logType;
    private TextFile textFile;
    // LogGenerator logGenerator;

    public LogCommand(String log, String logType, TextFile textFile) {
        this.log = log;
        this.logType = logType;
        this.textFile = textFile;
    }

    @Override
    public void execute() {
        // open file
        // textFile.open();
        // write to new line in file
        // save file

        textFile.open();
    }

}
