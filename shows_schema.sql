-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema shows_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema shows_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `shows_schema` DEFAULT CHARACTER SET utf8 ;
USE `shows_schema` ;

-- -----------------------------------------------------
-- Table `shows_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shows_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `shows_schema`.`shows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shows_schema`.`shows` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `network` VARCHAR(255) NULL,
  `release_date` DATE NULL,
  `description` VARCHAR(2000) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_shows_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_shows_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `shows_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `shows_schema`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shows_schema`.`likes` (
  `show_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  INDEX `fk_likes_shows1_idx` (`show_id` ASC) VISIBLE,
  INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_shows1`
    FOREIGN KEY (`show_id`)
    REFERENCES `shows_schema`.`shows` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `shows_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
