package com.example.thymeleaf.utilities;

public class StringMasker {
    public static String mask(String input) {
        if (input == null) {
            return null;
        }
        return "*".repeat(input.length());
    }
}
