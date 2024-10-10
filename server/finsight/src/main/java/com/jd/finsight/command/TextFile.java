package com.jd.finsight.command;

public class TextFile {
    private String filePath;

    public TextFile(String filePath) {
        this.filePath = filePath;
    }

    public void open() {
        System.out.println("opening file: " + this.filePath);
    }

    public void writeLine() {

    }

    public void save() {

    }

}
