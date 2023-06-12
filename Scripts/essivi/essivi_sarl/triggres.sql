create database essivi;
use essivi;
DELIMITER $$

CREATE TRIGGER mise_a_jour_stock_produit
AFTER INSERT
ON essivi_sarl_ligneentree FOR EACH ROW
BEGIN
    declare stock0 int;
    select stock into stock0 
    from essivi_sarl_produit 
    where essivi_sarl_produit.id=NEW.produit_id ;
    update essivi_sarl_produit 
    set essivi_sarl_produit.stock = stock0 + NEW.quantite
    where essivi_sarl_produit.id=NEW.produit_id ;
END$$

DELIMITER ;



DELIMITER $$
create procedure prix_ligne_commande(id integer,com_id int)
BEGIN
    declare prix0 float;
    select prix into prix0 
    from essivi_sarl_produit 
    where essivi_sarl_produit.id= id ;
    update essivi_sarl_lignecommande
    set essivi_sarl_lignecommande.prix = prix0 * essivi_sarl_lignecommande.quantite
    where essivi_sarl_lignecommande.id=com_id ;
END$$

DELIMITER ;



DELIMITER $$
CREATE TRIGGER mise_a_jour_commande
AFTER UPDATE
ON essivi_sarl_lignecommande FOR EACH ROW
BEGIN
    declare prix0 float;
    declare nombre int;
    select sum(prix) into prix0
    from essivi_sarl_lignecommande
    where essivi_sarl_lignecommande.commande_id = NEW.commande_id ;
    select count(id) into nombre
    from essivi_sarl_lignecommande
    where essivi_sarl_lignecommande.commande_id=NEW.commande_id ;
    update essivi_sarl_commande
    set essivi_sarl_commande.prix = prix0 
    where essivi_sarl_commande.id=NEW.commande_id ;
    update essivi_sarl_commande
    set essivi_sarl_commande.nombre_article = nombre 
    where essivi_sarl_commande.id=NEW.commande_id ;
END$$
DELIMITER ;


DELIMITER $$

CREATE TRIGGER mise_a_jour_produit
AFTER INSERT
ON essivi_sarl_lignecommande FOR EACH ROW
BEGIN
    declare stock0 int;
    select stock into stock0 
    from essivi_sarl_produit 
    where essivi_sarl_produit.id=NEW.produit_id ;
    update essivi_sarl_produit 
    set essivi_sarl_produit.stock = stock0 - NEW.quantite
    where essivi_sarl_produit.id=NEW.produit_id ;
END$$

DELIMITER ;

DELIMITER $$
create procedure livraison(distance float,id int,com int)
BEGIN
	declare delai datetime;
    select now() into delai;
    update essivi_sarl_livraison
    set essivi_sarl_livraison.prix = 50*distance
    where essivi_sarl_livraison.id=id ;
    update essivi_sarl_livraison
    set essivi_sarl_livraison.delai = date_add(delai,interval 30+3*distance minute)
    where essivi_sarl_livraison.id=id ;
    update essivi_sarl_livraison
    set essivi_sarl_livraison.distance = distance
    where essivi_sarl_livraison.id=id ;
    update essivi_sarl_commande
    set essivi_sarl_commande.statut="en cours"
    where essivi_sarl_commande.id=com;
END$$
DELIMITER ;



DELIMITER $$
create procedure facture(livr_id int,com_id int,client_id int ,prix_livr float)
BEGIN
	declare prix_commande float;
    declare total float;
    select prix into prix_commande
    from essivi_sarl_commande
    where essivi_sarl_commande.id=com_id;
    select (prix_livr+prix_commande) into total;
    insert into essivi_sarl_facture(livraison_id,commande_id,client_id,prix_com,prix_livr,prix_total,statut,date_ajout) values
    (livr_id,com_id,client_id,prix_commande,prix_livr,total,'nonpayée',now());
END$$

DELIMITER ;

DELIMITER $$
create procedure annulercommande(id varchar(10))
BEGIN
	update essivi_sarl_commande 
    set essivi_sarl_commande.statut ="annulée"
    where essivi_sarl_commande.id=id;
END$$

DELIMITER ;
DELIMITER $$
create procedure livraisonterminer(id_livr int,id_com int)
BEGIN
	update essivi_sarl_livraison 
    set essivi_sarl_livraison.statut ="ternimée"
    where id=id_livr;
	update essivi_sarl_commande 
	set essivi_sarl_commande.statut ="livrée"
	where id=id_com;
END$$

DELIMITER ;
DELIMITER $$
create procedure facturepaye(id_fact int)
BEGIN
	update essivi_sarl_facture 
    set essivi_sarl_facture.statut ="payée"
    where id=id_fact;
END$$

DELIMITER ;
CREATE DEFINER=`root`@`localhost` PROCEDURE `nom_client_commande`(id_com int,id_client int)
BEGIN
	declare nom_client  varchar(50);
    declare prenom_client varchar(50);
	select last_name ,first_name into nom_client,prenom_client
	from essivi_sarl_client
	where essivi_sarl_client.id=id_client;
    update essivi_sarl_commande
    set essivi_sarl_commande.client_name= concat(nom_client," ",prenom_client) 
    where essivi_sarl_commande.id=id_com;

END
CREATE DEFINER=`root`@`localhost` PROCEDURE `nom_client_livraison`(id_livr int,id_client int)
BEGIN
	declare nom_client  varchar(50);
    declare prenom_client varchar(50);
	select last_name ,first_name into nom_client,prenom_client
	from essivi_sarl_client
	where essivi_sarl_client.id=id_client;
    update essivi_sarl_livraison
    set essivi_sarl_livraison.client_name= concat(nom_client," ",prenom_client) 
    where essivi_sarl_livraison.id=id_livr;

END