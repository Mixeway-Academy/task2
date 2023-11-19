package com.example.thymeleaf.entity;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import javax.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Getter
@Setter
@Entity
@Table(name = "student")
@EqualsAndHashCode(of = {"id"})
public class Student {
    @Transient
    private static final Logger logger = LoggerFactory.getLogger(Student.class);
    @Id
    private String id;

    private String name;
    private String email;
    private LocalDate birthday;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @OneToOne(mappedBy = "student", cascade = CascadeType.ALL, orphanRemoval = true)
    private Address address;

    @PrePersist
    private void prePersist() {
        this.id = UUID.randomUUID().toString();
        this.createdAt = LocalDateTime.now();
        // W tym miejscu jest logowanie wrażliwych informacji po utworzeniu studenta
        logger.info("Created user {}", this);
    }

    @PreUpdate
    private void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }

    @Override
    public String toString() {
        // Zastąpienie wartości na '*'
        String id_hidden = "*".repeat(id.length());
        String name_hidden = "*".repeat(name.length());
        String email_hidden = "*".repeat(email.length());
        String birthday_hidden = String.valueOf(LocalDate.parse("*".repeat(birthday.toString().length())));
        String createdAt_hidden = String.valueOf(LocalDateTime.parse("*".repeat(createdAt.toString().length())));
        String updatedAt_hidden = String.valueOf(LocalDateTime.parse("*".repeat(updatedAt.toString().length())));
        String address_hidden = "*".repeat(address.length());

        return "Student{" +
                "id='" +  id_hidden + '\'' +
                ", name='" + name_hidden + '\'' +
                ", email='" + email_hidden + '\'' +
                ", birthday=" + birthday_hidden +
                ", createdAt=" + createdAt_hidden +
                ", updatedAt=" + updatedAt_hidden +
                ", address=" + address_hidden +
                '}';
    }
}
