SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS DBPRJ;
SET FOREIGN_KEY_CHECKS = 1;

CREATE DATABASE DBPRJ;
USE DBPRJ;

/* =============================================
   TABLE : ELEVE
   ============================================= */
CREATE TABLE ELEVE (
    id_eleve INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    date_naissance DATE NOT NULL,
    classe VARCHAR(20),
    sexe ENUM('M','F') NOT NULL,
    grp_sanguin ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-'),
    telephone_parent VARCHAR(15)
);

/* =============================================
   TABLE : DOSSIER_MEDICAL
   ============================================= */
CREATE TABLE DOSSIER_MEDICAL (
    id_dossier INT AUTO_INCREMENT PRIMARY KEY,
    id_eleve INT UNIQUE,
    antecedents TEXT,
    allergies TEXT,
    note_medicale INT,
    FOREIGN KEY (id_eleve) REFERENCES ELEVE(id_eleve),
    CHECK (note_medicale BETWEEN 1 AND 10)
);

/* =============================================
   TABLE : PERSONNEL_MEDICAL
   ============================================= */
CREATE TABLE PERSONNEL_MEDICAL (
    id_personnel INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    fonction ENUM('Infirmier','Medecin','Assistant') NOT NULL,
    matricule VARCHAR(50) NOT NULL,
    telephone VARCHAR(20) NOT NULL
);

/* =============================================
   TABLE : CONSULTATION
   ============================================= */
CREATE TABLE CONSULTATION (
    id_consultation INT AUTO_INCREMENT PRIMARY KEY,
    id_eleve INT,
    id_personnel INT,
    date_consultation DATE NOT NULL,
    type_consultation ENUM('Consultation','Urgence','Controle') NOT NULL,
    symptomes TEXT,
    diagnostic TEXT,
    decisions ENUM('Repos','Traitement','Transfert'),
    FOREIGN KEY (id_eleve) REFERENCES ELEVE(id_eleve),
    FOREIGN KEY (id_personnel) REFERENCES PERSONNEL_MEDICAL(id_personnel)
);

/* =============================================
   TABLE : PRESCRIPTION
   ============================================= */
CREATE TABLE PRESCRIPTION (
    id_prescription INT AUTO_INCREMENT PRIMARY KEY,
    id_consultation INT UNIQUE,
    instructions TEXT,
    FOREIGN KEY (id_consultation) REFERENCES CONSULTATION(id_consultation)
);

/* =============================================
   TABLE : MEDICAMENT
   ============================================= */
CREATE TABLE MEDICAMENT (
    id_medicament INT AUTO_INCREMENT PRIMARY KEY,
    nom_medicament VARCHAR(100) NOT NULL,
    effets_secondaires TEXT
);

/* =============================================
   TABLE : PRESCRIPTION_MEDICAMENT
   ============================================= */
CREATE TABLE PRESCRIPTION_MEDICAMENT (
    id_prescription INT,
    id_medicament INT,
    dose VARCHAR(50),
    frequence VARCHAR(50),
    duree VARCHAR(50),
    PRIMARY KEY (id_prescription, id_medicament),
    FOREIGN KEY (id_prescription) REFERENCES PRESCRIPTION(id_prescription),
    FOREIGN KEY (id_medicament) REFERENCES MEDICAMENT(id_medicament)
);

/* =============================================
   TABLE : RENDEZ_VOUS
   ============================================= */
CREATE TABLE RENDEZ_VOUS (
    id_rdv INT AUTO_INCREMENT PRIMARY KEY,
    id_eleve INT,
    id_personnel INT,
    date_rdv DATE NOT NULL,
    type_rdv ENUM('Consultation','Urgence','Controle') NOT NULL,
    statut ENUM('Planifie','Confirme','Annule','Termine') NOT NULL,
    FOREIGN KEY (id_eleve) REFERENCES ELEVE(id_eleve),
    FOREIGN KEY (id_personnel) REFERENCES PERSONNEL_MEDICAL(id_personnel)
);

/* =============================================
   TABLE : VACCINATION
   ============================================= */
CREATE TABLE VACCINATION (
    id_vaccination INT AUTO_INCREMENT PRIMARY KEY,
    id_eleve INT,
    id_personnel INT,
    nom_vaccin VARCHAR(50) NOT NULL,
    date_vaccin DATE NOT NULL,
    rappel_necessaire ENUM('OUI','NON') NOT NULL,
    FOREIGN KEY (id_eleve) REFERENCES ELEVE(id_eleve),
    FOREIGN KEY (id_personnel) REFERENCES PERSONNEL_MEDICAL(id_personnel)
);

/* ==================== INSERTIONS ==================== */

/* ELEVE */
INSERT INTO ELEVE (nom, prenom, date_naissance, classe, sexe, grp_sanguin, telephone_parent) VALUES
('Haddad', 'Youssef', '2010-03-14', '6A', 'M', 'A+', '0612345678'),
('Ait Ali', 'Amine', '2009-06-21', '6B', 'M', 'O+', '0654321876'),
('Benali', 'Sara', '2011-01-10', '5A', 'F', 'B+', '0678213456'),
('Mouh', 'Salma', '2010-11-05', '6C', 'F', 'AB+', '0622558899'),
('Najib', 'Khalid', '2008-12-20', '7A', 'M', 'O-', '0611458796'),
('El Idrissi', 'Rachid', '2009-04-19', '6B', 'M', 'A-', '0669874521'),
('Bourkia', 'Aya', '2011-07-23', '5A', 'F', 'B-', '0695842136'),
('Chakir', 'Imane', '2010-02-16', '6C', 'F', 'A+', '0677541230'),
('Saidi', 'Mehdi', '2008-09-01', '7B', 'M', 'AB-', '0669988774'),
('Nassiri', 'Lina', '2011-05-22', '5B', 'F', 'O+', '0612034050');

/* DOSSIER_MEDICAL */
INSERT INTO DOSSIER_MEDICAL (id_eleve, antecedents, allergies, note_medicale) VALUES
(1,'Asthme leger','Aucune',7),
(2,'Aucun probleme','Pollen',8),
(3,'Sinusite chronique','Arachides',6),
(4,'Migraine','Aucune',9),
(5,'Anemie','Oeufs',5),
(6,'Aucun probleme','Poussiere',8),
(7,'Diabete type 1','Aucune',4),
(8,'Aucun probleme','Lactose',7),
(9,'Cardiopathie leger','Aucune',6),
(10,'Aucun probleme','Aucune',9);

/* PERSONNEL_MEDICAL */
INSERT INTO PERSONNEL_MEDICAL (nom, prenom, fonction, matricule, telephone) VALUES
('El Fassi','Mouna','Infirmier','INF001','0611111111'),
('Karimi','Hassan','Medecin','MED001','0622222222'),
('Bouhssine','Samira','Infirmier','INF002','0633333333'),
('Yahyaoui','Omar','Medecin','MED002','0644444444'),
('Lamrani','Nawal','Assistant','ASS001','0655555555');

/* CONSULTATION */
INSERT INTO CONSULTATION (id_eleve,id_personnel,date_consultation,type_consultation,symptomes,diagnostic,decisions) VALUES
(1,1,'2025-01-12','Consultation','Toux legere','Rhume','Repos'),
(2,2,'2025-01-14','Urgence','Fievre 39','Infection virale','Traitement'),
(3,3,'2025-01-15','Consultation','Maux de tete','Migraine','Repos'),
(4,1,'2025-01-16','Controle','Controle general','RAS','Repos'),
(5,4,'2025-01-17','Urgence','Evanouissement','Anemie severe','Transfert'),
(6,2,'2025-01-18','Consultation','Douleurs ventre','Gastro','Traitement'),
(7,3,'2025-01-19','Controle','Suivi diabete','Glycemie elevee','Traitement'),
(8,1,'2025-01-20','Consultation','Toux seche','Allergie','Traitement'),
(9,4,'2025-01-21','Urgence','Douleur thoracique','Suspicion cardiaque','Transfert'),
(10,1,'2025-01-22','Consultation','Fievre legere','Infection','Traitement'),
(1,2,'2025-01-25','Consultation','Maux de gorge','Angine','Traitement'),
(3,3,'2025-01-25','Controle','Controle sinusite','Inflammation','Traitement'),
(7,4,'2025-01-26','Consultation','Fatigue','Hypoglycemie','Repos'),
(9,1,'2025-01-26','Consultation','Douleur jambe','Entorse','Repos'),
(10,3,'2025-01-27','Consultation','Toux','Bronchite','Traitement');

/* PRESCRIPTION */
INSERT INTO PRESCRIPTION (id_consultation,instructions) VALUES
(1,'Boire beaucoup deau'),
(2,'Repos et antipyretique'),
(3,'Eviter les ecrans'),
(6,'Hydratation et regime'),
(7,'Suivi medical quotidien'),
(8,'Eviter poussiere'),
(10,'Repos et vitamines'),
(11,'Antibiotiques 7 jours'),
(12,'Spray nasal'),
(15,'Traitement bronchite');

/* MEDICAMENT */
INSERT INTO MEDICAMENT (nom_medicament,effets_secondaires) VALUES
('Paracetamol','Somnolence'),
('Ibuprofene','Douleur estomac'),
('Vitamine C','Aucun'),
('Amoxicilline','Allergie possible'),
('Ventoline','Tremblements'),
('Doliprane','Somnolence'),
('Cetirizine','Somnolence'),
('Gaviscon','Ballonnement'),
('Omeprazole','Maux de tete'),
('Azithromycine','Nausees'),
('Insuline','Hypoglycemie'),
('Acide Folic','Aucun');

/* PRESCRIPTION_MEDICAMENT */
INSERT INTO PRESCRIPTION_MEDICAMENT VALUES
(1,1,'500mg','2 fois/jour','3 jours'),
(2,2,'400mg','2 fois/jour','5 jours'),
(2,3,'1 sachet','1 fois/jour','7 jours'),
(3,1,'500mg','1 fois/jour','2 jours'),
(6,8,'10ml','3 fois/jour','4 jours'),
(7,11,'10 unites','1 fois/jour','1 jour'),
(8,7,'5mg','1 fois/jour','10 jours'),
(10,3,'1 sachet','1 fois/jour','5 jours'),
(9,4,'500mg','2 fois/jour','7 jours'),
(10,10,'250mg','2 fois/jour','5 jours'),
(5,1,'500mg','1 fois/jour','3 jours'),
(6,6,'500mg','1 fois/jour','3 jours'),
(3,7,'5mg','1 fois/jour','5 jours'),
(1,3,'1 sachet','1 fois/jour','3 jours'),
(10,6,'500mg','2 fois/jour','4 jours'),
(8,1,'500mg','2 fois/jour','5 jours'),
(10,8,'10ml','3 fois/jour','2 jours'),
(9,5,'2 inhalations','3 fois/jour','2 jours'),
(7,9,'20mg','1 fois/jour','10 jours');

/* RENDEZ_VOUS */
INSERT INTO RENDEZ_VOUS (id_eleve,id_personnel,date_rdv,type_rdv,statut) VALUES
(1,1,'2025-02-01','Consultation','Planifie'),
(2,2,'2025-02-02','Urgence','Confirme'),
(3,3,'2025-02-03','Controle','Planifie'),
(4,1,'2025-02-04','Consultation','Annule'),
(5,4,'2025-02-06','Controle','Planifie'),
(6,2,'2025-02-06','Consultation','Confirme'),
(7,3,'2025-02-07','Controle','Planifie'),
(8,1,'2025-02-08','Consultation','Planifie'),
(9,4,'2025-02-09','Urgence','Confirme'),
(10,3,'2025-02-10','Consultation','Planifie'),
(1,2,'2025-02-12','Controle','Planifie'),
(7,4,'2025-02-13','Consultation','Confirme');

/* VACCINATION */
INSERT INTO VACCINATION (id_eleve,id_personnel,nom_vaccin,date_vaccin,rappel_necessaire) VALUES
(1,1,'BCG','2025-01-10','NON'),
(2,2,'Grippe','2025-01-12','OUI'),
(3,3,'Tetanos','2025-01-13','NON'),
(4,1,'Grippe','2025-01-14','OUI'),
(5,4,'Hepatite B','2025-01-15','NON'),
(6,2,'Covid19','2025-01-16','OUI'),
(7,3,'Hepatite A','2025-01-17','NON'),
(8,1,'Grippe','2025-01-18','OUI'),
(9,4,'Covid19','2025-01-19','NON'),
(10,3,'BCG','2025-01-20','NON');


ALTER TABLE PERSONNEL_MEDICAL 
MODIFY fonction VARCHAR(50);
