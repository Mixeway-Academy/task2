package com.example.thymeleaf.util;

public final class MaskingUtils {

    private MaskingUtils() {
    }
    public static String mask(Object value) {
        return value == null ? "null" : "*".repeat(value.toString().length());
    }
}
