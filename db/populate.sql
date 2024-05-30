INSERT INTO `VISITATORI` (`CodiceFiscale`, `Nome`, `Cognome`, `DataDiNascita`, `Altezza`, `Peso`) VALUES
('RSSMRA85M01H501Z', 'Mario', 'Rossi', '1985-06-01', 175, 70.2),
('VRDLGI75D18H501Y', 'Luigi', 'Verdi', '1975-04-18', 180, 82.1),
('BNCLRA90A01F205X', 'Laura', 'Bianchi', '1990-01-01', 165, 58.3),
('FRNMNL88C20D612X', 'Manuela', 'Ferrari', '1988-03-20', 160, 55.0),
('BLUGPP80B30A111X', 'Giuseppe', 'Blu', '1980-02-28', 190, 90.5),
('RTTLUC95E14G222Z', 'Lucia', 'Ratti', '1995-05-14', 170, 65.7),
('NTTFBN70F11H501X', 'Fabiano', 'Neri', '1970-06-11', 178, 72.4),
('CRLSLV88D22H703X', 'Silvia', 'Carli', '1988-04-22', 160, 50.3),
('MNNLRA78C21G273Z', 'Lara', 'Manni', '1978-03-21', 172, 68.1),
('GRSLGI85A15F987X', 'Giorgio', 'Giraldi', '1985-01-15', 185, 75.6),
('GRNLUI83E10D734X', 'Luigi', 'Giornaldi', '1983-05-10', 167, 69.4),
('BNCLDR80B01E111Z', 'Loredana', 'Bianchi', '1980-02-01', 162, 52.7),
('RSSMRA92G23H501X', 'Marco', 'Rossi', '1992-07-23', 176, 74.2),
('FRNMNL87C20D612X', 'Michela', 'Ferrari', '1987-03-20', 162, 54.0),
('BLUGPP79B30A111X', 'Giovanni', 'Blu', '1979-02-15', 188, 88.3),
('RTTLUC96E14G222Z', 'Lucrezia', 'Ratti', '1996-05-14', 172, 66.0),
('NTTFBN69F11H501X', 'Fabrizio', 'Neri', '1969-06-11', 180, 76.4),
('CRLSLV89D22H703X', 'Simona', 'Carli', '1989-04-22', 161, 51.5),
('MNNLRA77C21G273Z', 'Elena', 'Manni', '1977-03-21', 175, 70.1),
('GRSLGI86A15F987X', 'Gabriele', 'Giraldi', '1986-01-15', 186, 77.6);


INSERT INTO `DURATE` (`Giorni`, `Sconto`, `Descrizione`) VALUES
(1, 0.0, 'Giornaliero'),
(7, 0.5, 'Settimanale'),
(14, 1.0, 'Bisettimanale'),
(30, 2.0, 'Mensile'),
(90, 5.0, 'Trimestrale'),
(180, 10.0, 'Semestrale'),
(365, 20.0, 'Annuale');

INSERT INTO `TARIFFE` (`Nome`, `CostoGiornaliero`) VALUES
('Standard', 10.0),
('Bronze', 12.0),
('Silver', 15.0),
('Gold', 20.0),
('Platinum', 25.0),
('Diamond', 30.0),
('VIP', 50.0);