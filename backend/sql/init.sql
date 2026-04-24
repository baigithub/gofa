-- Gofer 初始化 SQL（MySQL 8.0）
-- 用法：
--   docker exec -i gofer-mysql mysql -uroot -proot123456 < backend/sql/init.sql

CREATE DATABASE IF NOT EXISTS `gofer`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `gofer`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS `users` (
  `id` CHAR(36) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `nickname` VARCHAR(50) NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'user',
  `is_enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_phone` (`phone`),
  KEY `ix_users_phone` (`phone`),
  KEY `ix_users_role` (`role`),
  KEY `ix_users_is_enabled` (`is_enabled`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `roles` (
  `id` CHAR(36) NOT NULL,
  `code` VARCHAR(20) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `description` TEXT NULL,
  `is_enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_roles_code` (`code`),
  KEY `ix_roles_code` (`code`),
  KEY `ix_roles_is_enabled` (`is_enabled`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `runner_profiles` (
  `id` CHAR(36) NOT NULL,
  `user_id` CHAR(36) NOT NULL,
  `student_no` VARCHAR(32) NULL,
  `is_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_runner_profiles_user_id` (`user_id`),
  KEY `ix_runner_profiles_user_id` (`user_id`),
  CONSTRAINT `fk_runner_profiles_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `addresses` (
  `id` CHAR(36) NOT NULL,
  `user_id` CHAR(36) NOT NULL,
  `label` VARCHAR(50) NULL,
  `detail` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_addresses_user_id` (`user_id`),
  CONSTRAINT `fk_addresses_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `orders` (
  `id` CHAR(36) NOT NULL,
  `user_id` CHAR(36) NOT NULL,
  `runner_id` CHAR(36) NULL,
  `order_type` VARCHAR(20) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `pickup_address` VARCHAR(255) NULL,
  `delivery_address` VARCHAR(255) NULL,
  `contact_phone` VARCHAR(20) NOT NULL,
  `remark` TEXT NULL,
  `amount_cents` INT NOT NULL DEFAULT 0,
  `required_completed_at` DATETIME NULL,
  `completed_at` DATETIME NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_orders_user_id` (`user_id`),
  KEY `ix_orders_runner_id` (`runner_id`),
  KEY `ix_orders_status` (`status`),
  CONSTRAINT `fk_orders_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_orders_runner_id` FOREIGN KEY (`runner_id`) REFERENCES `runner_profiles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `order_status_logs` (
  `id` CHAR(36) NOT NULL,
  `order_id` CHAR(36) NOT NULL,
  `from_status` VARCHAR(20) NULL,
  `to_status` VARCHAR(20) NOT NULL,
  `note` VARCHAR(255) NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_order_status_logs_order_id` (`order_id`),
  CONSTRAINT `fk_order_status_logs_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `payments` (
  `id` CHAR(36) NOT NULL,
  `order_id` CHAR(36) NOT NULL,
  `provider` VARCHAR(20) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `amount_cents` INT NOT NULL DEFAULT 0,
  `provider_txn_id` VARCHAR(64) NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_payments_order_id` (`order_id`),
  KEY `ix_payments_order_id` (`order_id`),
  KEY `ix_payments_status` (`status`),
  CONSTRAINT `fk_payments_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `messages` (
  `id` CHAR(36) NOT NULL,
  `user_id` CHAR(36) NOT NULL,
  `order_id` CHAR(36) NULL,
  `title` VARCHAR(100) NOT NULL,
  `content` TEXT NOT NULL,
  `is_read` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_messages_user_id` (`user_id`),
  KEY `ix_messages_order_id` (`order_id`),
  CONSTRAINT `fk_messages_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_messages_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

