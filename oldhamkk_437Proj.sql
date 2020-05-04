-- phpMyAdmin SQL Dump
-- version 4.0.10deb1ubuntu0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 04, 2020 at 03:50 AM
-- Server version: 5.5.62-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `oldhamkk_437Proj`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE IF NOT EXISTS `customers` (
  `UID` int(5) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phonenumber` varchar(12) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL,
  `admin` varchar(5) NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`UID`, `fname`, `lname`, `address`, `phonenumber`, `password`, `email`, `admin`) VALUES
(1, 'John ', 'Smith', '123 ABC Drive', '907-888-9999', '123', 'a@a.com', 'True'),
(4, 'Sally', 'Seahorse', 'Jupiter Drive', '907-777-4545', '000', 'b@b.com', 'False'),
(3, 'Ken', 'Apple', '3650 Lake Otis Parkway Suite #102', '907-555-6666', '456', 'c@c.com', 'False');

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE IF NOT EXISTS `events` (
  `EID` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `VenueID` int(5) NOT NULL,
  PRIMARY KEY (`EID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`EID`, `name`, `start`, `end`, `VenueID`) VALUES
(1, 'Clarkson VS Cornell', '2020-05-03 19:30:00', '2020-05-03 21:00:00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE IF NOT EXISTS `ticket` (
  `TID` int(5) NOT NULL AUTO_INCREMENT,
  `section` varchar(4) NOT NULL,
  `row` varchar(4) NOT NULL,
  `available` varchar(5) NOT NULL,
  `handicap` varchar(5) NOT NULL,
  `type` varchar(4) NOT NULL,
  `box` varchar(5) NOT NULL,
  `EventID` varchar(100) NOT NULL,
  `UserID` varchar(5) NOT NULL,
  PRIMARY KEY (`TID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`TID`, `section`, `row`, `available`, `handicap`, `type`, `box`, `EventID`, `UserID`) VALUES
(1, '100', '12', 'True', 'True', 'True', 'True', '1', '1'),
(2, '120', '13', 'True', 'True', 'Fals', 'True', '1', '1'),
(3, '102', '3', 'True', 'False', 'True', 'False', '1', '1'),
(4, '100', '13', 'True', 'True', 'True', 'True', '1', '3');

-- --------------------------------------------------------

--
-- Table structure for table `Venue`
--

CREATE TABLE IF NOT EXISTS `Venue` (
  `VenueName` varchar(50) NOT NULL,
  `VenueID` int(5) NOT NULL AUTO_INCREMENT,
  `VenueAddress` varchar(100) NOT NULL,
  `VenueCollege` varchar(50) NOT NULL,
  `VenuePhoneNumber` char(12) NOT NULL,
  PRIMARY KEY (`VenueID`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `Venue`
--

INSERT INTO `Venue` (`VenueName`, `VenueID`, `VenueAddress`, `VenueCollege`, `VenuePhoneNumber`) VALUES
('Cheel Arena', 1, '8 Clarkson Ave, Potsdam, NY', 'Clarkson University', '315-268-7750');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
