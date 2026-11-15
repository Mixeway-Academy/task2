package com.example.thymeleaf.util;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class MaskUtil {

    public static String mask(String value) {
        if (value == null) {
            return null;
        }
        return "*".repeat(value.length());
    }
}
