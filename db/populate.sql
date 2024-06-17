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

INSERT INTO `TARIFFE` (`NomeTariffa`, `CostoGiornaliero`) VALUES
('Standard', 10.0),
('Bronze', 12.0),
('Silver', 15.0),
('VIP', 50.0);

INSERT INTO `ABBONAMENTI` (`CodiceFiscale`, `DataInizio`, `Costo`, `NomeTariffa`, `Giorni`) VALUES
('RSSMRA85M01H501Z', '2024-05-30', 10.0, 'Standard', 1),
('RSSMRA85M01H501Z', '2020-01-30', 10.0, 'Standard', 30),
('RSSMRA85M01H501Z', '2021-05-30', 10.0, 'Standard', 30),
('RSSMRA85M01H501Z', '2023-04-30', 10.0, 'Standard', 30),
('VRDLGI75D18H501Y', '2024-05-30', 12.0, 'Bronze', 7),
('BNCLRA90A01F205X', '2024-05-30', 15.0, 'Silver', 14),
('FRNMNL88C20D612X', '2024-05-30', 20.0, 'Silver', 30),
('BLUGPP80B30A111X', '2024-05-30', 25.0, 'Silver', 90),
('RTTLUC95E14G222Z', '2024-05-30', 30.0, 'VIP', 180),
('NTTFBN70F11H501X', '2024-05-30', 50.0, 'VIP', 365),
('CRLSLV88D22H703X', '2024-05-30', 10.0, 'Standard', 1),
('MNNLRA78C21G273Z', '2024-05-30', 10.0, 'Standard', 30),
('GRSLGI85A15F987X', '2024-05-30', 10.0, 'Standard', 30),
('GRNLUI83E10D734X', '2024-05-30', 12.0, 'Bronze', 7),
('BNCLDR80B01E111Z', '2024-05-30', 15.0, 'Silver', 14),
('RSSMRA92G23H501X', '2024-05-30', 20.0, 'Bronze', 30),
('FRNMNL87C20D612X', '2024-05-30', 25.0, 'VIP', 90),
('BLUGPP79B30A111X', '2024-05-30', 30.0, 'VIP', 180),
('RTTLUC96E14G222Z', '2024-05-30', 50.0, 'VIP', 365),
('NTTFBN69F11H501X', '2024-05-30', 10.0, 'Standard', 1),
('CRLSLV89D22H703X', '2024-05-30', 10.0, 'Standard', 30),
('MNNLRA77C21G273Z', '2024-05-30', 10.0, 'Standard', 30),
('GRSLGI86A15F987X', '2024-05-30', 12.0, 'Bronze', 7);

INSERT INTO `INGRESSI` (`CodiceFiscale`, `Data`) VALUES
('BLUGPP79B30A111X','2024-06-17'),
('BLUGPP79B30A111X','2024-06-19'),
('BLUGPP79B30A111X','2024-06-30'),
('BLUGPP80B30A111X','2024-06-17'),
('BLUGPP80B30A111X','2024-06-18'),
('BLUGPP80B30A111X','2024-06-19'),
('BLUGPP80B30A111X','2024-06-25'),
('BLUGPP80B30A111X','2024-06-29'),
('BLUGPP80B30A111X','2024-07-02'),
('CRLSLV88D22H703X','2024-06-17'),
('CRLSLV89D22H703X','2024-06-17'),
('CRLSLV89D22H703X','2024-06-23'),
('FRNMNL88C20D612X','2024-06-17'),
('FRNMNL88C20D612X','2024-06-23'),
('FRNMNL88C20D612X','2024-06-24'),
('FRNMNL88C20D612X','2024-06-26'),
('GRSLGI85A15F987X','2024-06-18'),
('GRSLGI85A15F987X','2024-06-27'),
('GRSLGI85A15F987X','2024-06-28'),
('GRSLGI85A15F987X','2024-06-29'),
('MNNLRA77C21G273Z','2024-06-28'),
('MNNLRA77C21G273Z','2024-06-29'),
('MNNLRA78C21G273Z','2024-06-27'),
('NTTFBN70F11H501X','2024-06-17'),
('NTTFBN70F11H501X','2024-06-23'),
('NTTFBN70F11H501X','2024-06-26'),
('NTTFBN70F11H501X','2024-06-27'),
('NTTFBN70F11H501X','2024-07-01'),
('RSSMRA85M01H501Z','2023-05-10'),
('RSSMRA85M01H501Z','2023-05-11'),
('RSSMRA85M01H501Z','2023-05-12'),
('RSSMRA92G23H501X','2024-06-17'),
('RSSMRA92G23H501X','2024-06-18'),
('RSSMRA92G23H501X','2024-06-19'),
('RSSMRA92G23H501X','2024-06-28'),
('RTTLUC95E14G222Z','2024-06-18'),
('RTTLUC95E14G222Z','2024-06-25'),
('RTTLUC95E14G222Z','2024-06-26'),
('RTTLUC95E14G222Z','2024-07-03'),
('RTTLUC95E14G222Z','2024-08-15'),
('RTTLUC96E14G222Z','2024-06-17'),
('RTTLUC96E14G222Z','2024-06-18'),
('RTTLUC96E14G222Z','2024-06-19'),
('RTTLUC96E14G222Z','2024-06-23'),
('RTTLUC96E14G222Z','2024-06-25'),
('RTTLUC96E14G222Z','2024-06-26'),
('RTTLUC96E14G222Z','2024-06-27');

INSERT INTO `LIMITI` (`Attributo`, `Condizione`, `Valore`, `Descrizione`) VALUES
('Altezza', '>', '140', 'Altezza maggiore di 140 cm'),
('DataDiNascita', '>=', '18', 'Solo maggiorenni'),
('DataDiNascita', '>', '14', 'Età maggiore di 14 anni'),
('Peso', '>', '40', 'Peso maggiore di 40 kg'),
('Peso', '<', '140', 'Peso minore di 140 kg');

INSERT INTO `CATEGORIE` (`Nome`) VALUES
('Roller Coasters'),
('Acqua'),
('Space Shot'),
('Laser Game'),
('Classica'),
('Giostra'),
('Simulatori'),
('Sala Giochi'),
('Parco Giochi');

INSERT INTO `ATTIVITA` (`Nome`, `Descrizione`, `Posti`, `IsEvent`, `IdCategoria`) VALUES
('Katun', 'Una delle montagne russe invertite più lunghe d''Europa, con curve ad alta velocità e inversioni mozzafiato.', 28, False, 1),
('Divertical', 'Il più alto water coaster del mondo, che combina elementi di montagne russe con un''emozionante discesa in acqua.', 10, False, 2),
('iSpeed', 'Montagne russe lanciate che accelerano da 0 a 100 km/h in pochi secondi, offrendo un''esperienza adrenalinica.', 12, False, 1),
('Oil Towers', 'Torri di caduta libera che offrono una vista panoramica prima di una discesa vertiginosa.', 16, False, 3),
('Master Thai VR', 'Montagne russe a doppio binario con l''aggiunta di realtà virtuale per un''esperienza immersiva.', 12, False, 7),
('Reset', 'Dark ride ambientata in una New York post-apocalittica, dove i visitatori devono sparare a bersagli per accumulare punti.', 4, False, 4),
('Leprotto Express', 'Montagne russe per famiglie, ideali per i più piccoli che vogliono provare l''emozione di una corsa in sicurezza.', 20, False, 5),
('Monosauro', 'Giostra per bambini a tema dinosauri, con veicoli che seguono un percorso su rotaia.', 6, False, 5),
('Carousel', 'Giostra classica con cavalli e carrozze colorate, perfetta per tutte le età.', 30, False, 6),
('Rexplorer', 'Attrazione tematica che porta i visitatori in un viaggio esplorativo tra i dinosauri.', 4, False, 5),
('Pakal', 'Montagne russe minori che offrono curve e discese emozionanti in uno spazio compatto.', 20, False, 1),
('Auto Splash', 'Attrazione acquatica che combina elementi di un percorso a ostacoli con splash finali.', 6, False, 2),
('Eurowheel', 'Una delle ruote panoramiche più alte d''Europa, che offre una vista mozzafiato sul parco e dintorni.', 8, False, 6),
('Ducati World', 'Area tematica dedicata al marchio Ducati, con simulatori e attrazioni ispirate alle moto.', 2, False, 7),
('Raratonga', 'Attrazione acquatica interattiva con pistole ad acqua, ideale per tutta la famiglia.', 8, False, 2),
('Rio Bravo', 'Rafting ride che porta i visitatori lungo un fiume con rapide e spruzzi.', 6 , False, 2),
('Brontocars', 'Percorso di guida per bambini, con auto elettriche che seguono un percorso su rotaia.', 1, False, 5),
('Explorer', 'Giostra a tema safari che simula un''avventura nella giungla.', 16, False, 6),
('Santa Fe Express', 'Trenino panoramico che attraversa diverse aree del parco, offrendo una piacevole vista delle attrazioni.', 40, False, 6),
('Phobia', 'Attrazione interattiva con effetti speciali che immergono i visitatori in un''esperienza spaventosa.', 8, False, 7),
('Grosso Guaio a Stunt City', 'Spettacolo di stunt con automobili, moto e acrobazie mozzafiato.', 200, True, NULL),
('Hot Wheels City: La nuova sfida', 'Spettacolo di acrobazie e stunt ispirato al mondo Hot Wheels, con auto e moto che eseguono numeri incredibili.', 200, True, NULL),
('Magic Halloween', 'Evento stagionale con decorazioni, spettacoli a tema Halloween e personaggi in costume.', 500, True, NULL),
('Christmas Time', 'Evento natalizio con decorazioni a tema, spettacoli, mercatini e attività festive.', 500, True, NULL);

INSERT INTO `VINCOLA` (`IdLimite`, `IdAttivita`) VALUES
(1, 1),  -- Katun
(3, 1),  -- Katun
(4, 1),  -- Katun
(1, 2),  -- Divertical
(5, 2),  -- Divertical
(1, 3),  -- iSpeed
(3, 3),  -- iSpeed
(4, 3),  -- iSpeed
(5, 3),  -- iSpeed
(1, 4),  -- Oil Towers
(4, 4),  -- Oil Towers
(1, 5),  -- Master Thai VR
(4, 5),  -- Master Thai VR
(3, 6),  -- Reset
(1, 7),  -- Leprotto Express
(5, 9),  -- Carousel
(1, 11), -- Pakal
(3, 11), -- Pakal
(4, 11), -- Pakal
(5, 11), -- Pakal
(4, 12), -- Auto Splash
(5, 12), -- Auto Splash
(5, 13), -- Eurowheel
(5, 15), -- Raratonga
(5, 16), -- Rio Bravo
(5, 17), -- Brontocars
(2, 20); -- Phobia

INSERT INTO `PROGRAMMAZIONI` (`IdAttivita`, `Data`, `Inizio`, `Fine`) VALUES
(21, '2024-05-30', '10:00:00', '12:00:00'),
(21, '2024-05-30', '14:00:00', '16:00:00'),
(21, '2024-06-04', '10:00:00', '12:00:00'),
(21, '2024-06-04', '14:00:00', '16:00:00'),
(21, '2024-06-06', '10:00:00', '12:00:00'),
(21, '2024-06-06', '14:00:00', '16:00:00'),
(21, '2024-06-11', '10:00:00', '12:00:00'),
(21, '2024-06-11', '14:00:00', '16:00:00'),
(21, '2024-06-13', '10:00:00', '12:00:00'),
(21, '2024-06-13', '14:00:00', '16:00:00'),
(21, '2024-06-18', '10:00:00', '12:00:00'),
(21, '2024-06-18', '14:00:00', '16:00:00'),
(21, '2024-06-20', '10:00:00', '12:00:00'),
(21, '2024-06-20', '14:00:00', '16:00:00'),
(21, '2024-06-25', '10:00:00', '12:00:00'),
(21, '2024-06-25', '14:00:00', '16:00:00'),
(21, '2024-06-27', '10:00:00', '12:00:00'),
(21, '2024-06-27', '14:00:00', '16:00:00'),
(21, '2024-07-01', '10:00:00', '12:00:00'),
(21, '2024-07-01', '14:00:00', '16:00:00'),
(21, '2024-07-04', '10:00:00', '12:00:00'),
(21, '2024-07-04', '14:00:00', '16:00:00'),
(22, '2024-06-02', '13:00:00', '17:00:00'),
(22, '2024-06-09', '13:00:00', '17:00:00'),
(22, '2024-06-16', '13:00:00', '17:00:00'),
(22, '2024-06-23', '13:00:00', '17:00:00'),
(22, '2024-06-30', '13:00:00', '17:00:00'),
(22, '2024-07-07', '13:00:00', '17:00:00'),
(23, '2024-10-04', '19:00:00', '24:00:00'),
(23, '2024-10-05', '20:00:00', '01:00:00'),
(23, '2024-10-11', '19:00:00', '24:00:00'),
(23, '2024-10-12', '20:00:00', '01:00:00'),
(23, '2024-10-18', '19:00:00', '24:00:00'),
(23, '2024-10-19', '20:00:00', '01:00:00'),
(23, '2024-10-25', '19:00:00', '24:00:00'),
(23, '2024-10-26', '20:00:00', '01:00:00'),
(23, '2024-10-30', '19:00:00', '24:00:00'),
(23, '2024-10-31', '20:00:00', '01:00:00'),
(23, '2024-11-01', '19:00:00', '24:00:00'),
(24, '2024-12-08', '10:00:00', '16:00:00'),
(24, '2024-12-15', '10:00:00', '16:00:00'),
(24, '2024-12-22', '10:00:00', '16:00:00'),
(24, '2024-12-29', '10:00:00', '16:00:00');

INSERT INTO `PARTECIPA` (`IdIngresso`, `Ora`, `IdAttivita`) VALUES
(1, '10:00:00', 1);

INSERT INTO `INCLUDE` (`IdTariffa`, `IdCategoria`) VALUES 
(1, 1),  -- Standard include Roller Coasters
(1, 2),  -- Standard include Acqua
(1, 3),  -- Standard include Space Shot
(2, 1),  -- Bronze include Roller Coasters
(2, 2),  -- Bronze include Acqua
(2, 3),  -- Bronze include Space Shot
(2, 4),  -- Bronze include Laser Game
(2, 5),  -- Bronze include Classica
(3, 1),  -- Silver include Roller Coasters
(3, 2),  -- Silver include Acqua
(3, 3),  -- Silver include Space Shot
(3, 4),  -- Silver include Laser Game
(3, 5),  -- Silver include Classica
(3, 6),  -- Silver include Giostra
(3, 7),  -- Silver include Simulatori
(4, 1),  -- VIP include Roller Coasters
(4, 2),  -- VIP include Acqua
(4, 3),  -- VIP include Space Shot
(4, 4),  -- VIP include Laser Game
(4, 5),  -- VIP include Classica
(4, 6),  -- VIP include Giostra
(4, 7),  -- VIP include Simulatori
(4, 8),  -- VIP include Sala Giochi
(4, 9);  -- VIP include Parco Giochi

INSERT INTO `RUOLI` (`Nome`, `Stipendio`) VALUES
('Responsabile alle Attrazioni', 3000.0),
('Addetto alle Attrazioni', 1500.0),
('Addetto alla Sicurezza', 1800.0),
('Operatore di Giostra', 1400.0),
('Addetto alle Pulizie', 1200.0),
('Addetto alla Biglietteria', 1300.0),
('Animatore', 1400.0),
('Tecnico del Suono e Luci', 1600.0),
('Tecnico di Manutenzione', 1700.0),
('Commesso', 1300.0),
('Cassiere', 1250.0),
('Magazziniere', 1350.0),
('Cuoco', 1600.0),
('Cameriere', 1200.0),
('Responsabile di Negozio', 2000.0),
('Soccorritore', 1500.0);

INSERT INTO `ORARI` (`Lunedi`, `Martedi`, `Mercoledi`, `Giovedi`, `Venerdi`, `Sabato`, `Domenica`) VALUES
('10:00-18:00', '10:00-18:00', '10:00-18:00', '10:00-18:00', '10:00-20:00', '10:00-20:00', '10:00-18:00'),
('09:00-17:00', '09:00-17:00', '09:00-17:00', '09:00-17:00', '09:00-19:00', '09:00-19:00', '09:00-17:00'),
('11:00-19:00', '11:00-19:00', '11:00-19:00', '11:00-19:00', '11:00-21:00', '11:00-21:00', '11:00-19:00'),
('08:00-16:00', '08:00-16:00', '08:00-16:00', '08:00-16:00', '08:00-18:00', '08:00-18:00', '08:00-16:00');

INSERT INTO `SERVIZI` (`Nome`, `Tipo`, `IdOrario`) VALUES
('WC - Nord', 'Toilette', '1'),
('WC - Est', 'Toilette', '1'),
('WC - Ovest', 'Toilette', '1'),
('WC - Sud', 'Toilette', '1'),
('Pesciolini allo spiedo', 'Ristoro', 1),
('Mustafa Kebab', 'Ristoro', 2),
('McDonald', 'Ristoro', 3),
('Pizzeria Ciro', 'Ristoro', 4),
('Gelatino', 'Ristoro', 1),
('Souvenirs', 'Negozio', 2),
('Fiori Rossi', 'Negozio', 2),
('OVS', 'Negozio', '1'),
('Terranova', 'Negozio', '1'),
('Pull & Bear', 'Negozio', '1'),
('Feltrinelli', 'Negozio', 1);

-- NECESSITA
INSERT INTO `NECESSITA` (`IdCategoria`, `IdRuolo`, `Quantita`) VALUES
(1, 2, 5),  -- Necessità per 5 Addetti alle Attrazioni per le Montagne Russe
(2, 4, 4),  -- Necessità per 4 Operatori di Giostra per le Attrazioni Acquatiche
(3, 2, 3),  -- Necessità per 3 Addetti alle Attrazioni per le Torri di Caduta
(4, 4, 2),  -- Necessità per 2 Operatori di Giostra per le Dark Ride
(5, 2, 4),  -- Necessità per 4 Addetti alle Attrazioni per le Attrazioni per Bambini
(6, 2, 3),  -- Necessità per 3 Addetti alle Attrazioni per le Giostre Classiche
(7, 8, 2);  -- Necessità per 2 Tecnici del Suono e Luci per le Attrazioni di Realtà Virtuale

-- PERSONALE 
INSERT INTO `PERSONALE` (`CodiceFiscale`, `Nome`, `Cognome`, `DataDiNascita`, `IdRuolo`, `IdServizio`) VALUES
('RSSMRA85M01H501Z', 'Marco', 'Rossi', '1985-01-01', 1, NULL),  -- Responsabile alle Attrazioni, Necessita, quindi IdServizio è NULL
('BLNLNZ80A01H501Z', 'Lorenzo', 'Bianchi', '1980-01-01', 2, NULL),  -- Addetto alle Attrazioni, Necessita, quindi IdServizio è NULL
('VRDGNN75B01F205X', 'Gianna', 'Verdi', '1975-02-01', 3, NULL),  -- Addetto alla Sicurezza, Necessita, quindi IdServizio è NULL
('FRRFRC90C15H501Y', 'Francesco', 'Ferrari', '1990-03-15', 4, NULL),  -- Operatore di Giostra, Necessita, quindi IdServizio è NULL
('GLLMRL92D01H501J', 'Mirella', 'Galli', '1992-04-01', 5, 1),  -- Addetto alle Pulizie, non Necessita, assegnato a WC - Nord
('RSLTNC88E01H501K', 'Tania', 'Russo', '1988-05-01', 6, 10),  -- Addetto alla Biglietteria, non Necessita, assegnato a Souvenirs
('MRTLBR81F01H501L', 'Lorenzo', 'Martini', '1981-06-01', 7, NULL),  -- Animatore, Necessita, quindi IdServizio è NULL
('FNTMRL87G01H501M', 'Marco', 'Fantini', '1987-07-01', 8, NULL),  -- Tecnico del Suono e Luci, Necessita, quindi IdServizio è NULL
('SRLMCL94H01H501N', 'Michele', 'Sarli', '1994-08-01', 9, NULL),  -- Tecnico di Manutenzione, Necessita, quindi IdServizio è NULL
('GNFMRT85I01H501P', 'Martina', 'Gennari', '1985-09-01', 10, 14),  -- Commesso, non Necessita, assegnato a Pull & Bear
('RLLFLC83J01H501Q', 'Federico', 'Rallo', '1983-10-01', 11, 12),  -- Cassiere, non Necessita, assegnato a OVS
('PNTLBR89K01H501R', 'Laura', 'Pintus', '1989-11-01', 12, NULL),  -- Magazziniere, Necessita, quindi IdServizio è NULL
('BRTGRG77L01H501S', 'Giorgio', 'Baratta', '1977-12-01', 13, 6),  -- Cuoco, non Necessita, assegnato a Mustafa Kebab
('VNTMRL90M01H501T', 'Mario', 'Vincenti', '1990-01-01', 14, 7),  -- Cameriere, non Necessita, assegnato a McDonald
('BRNMRC87P01H501W', 'Marco', 'Bruni', '1987-04-01', 15, 11),  -- Responsabile di Negozio, non Necessita, assegnato a Fiori Rossi
('ZNNLCR85Q01H501X', 'Lucia', 'Zanini', '1985-05-01', 16, NULL),  -- Soccorritore, Necessita, quindi IdServizio è NULL
('MNCLRC92R01H501Y', 'Lorenzo', 'Mancini', '1992-06-01', 10, 13),  -- Commesso, non Necessita, assegnato a Terranova
('GRGFRN90S01H501Z', 'Francesco', 'Gregori', '1990-07-01', 5, 2);  -- Addetto alle Pulizie, non Necessita, assegnato a WC - Est

