import unittest
import os
import neo4j

class TestBdg(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        URI = os.getenv('NEO4J_URL')
        user = os.getenv('NEO4J_USERNAME')
        password = os.getenv('NEO4J_PASSWORD')
        AUTH = (user, password)
        self.driver = neo4j.GraphDatabase.driver(URI, auth=AUTH)
        
        self.msg = "la règle '{0}' n'est pas respectée."
        
        
    @classmethod
    def tearDownClass(self):
        self.driver.close()
        
        
    def test_0_Connectivity(self):
        self.driver.verify_connectivity()
        
    def test_1_Concepts(self):
        regle = """le libellé d'un concept est un texte non vide"""
        req = """
        MATCH (c:Concept)
        WHERE c.litteral IS NULL OR c.litteral <> toStringOrNull(c.litteral)
        RETURN count(c) = 0 AS bool
            """
        msg = self.msg.format(regle)
        records, summary, keys = self.driver.execute_query(req)
        self.assertTrue(records[0].data()['bool'] ,msg)
        
    def test_2_Concepts(self):
        regle = """un concept est caractérisé par son type et son libellé"""
        req = """
        MATCH (n1:Concept),(n2:Concept)
        WHERE n1.typeConcept = n2.typeConcept 
            AND n1.litteral = n2.litteral 
            AND id(n1) < id(n2)
        RETURN count(*) = 0  AS bool  
            """
        msg = self.msg.format(regle)
        records, summary, keys = self.driver.execute_query(req)
        self.assertTrue(records[0].data()['bool'],msg)
        
    def test_10_Documents(self):
        regle = """Un noeud document est caractérisé par son type et son titre"""
        req = """
            MATCH (n1:Document),(n2:Document)
                WHERE n1.typeDoc = n2.typeDoc  
                    AND n1.titre = n2.titre AND id(n1) < id(n2)
            RETURN count(*) = 0 AS bool
            """
        msg = self.msg.format(regle)
        records, summary, keys = self.driver.execute_query(req)
        self.assertTrue(records[0].data()['bool'],msg)

    def test_100_Evenement(self):
        regle = """Un noeud événement est caractérisé par son type et son nom"""
        req = """
            MATCH (n1:Evenement),(n2:Evenement)
                WHERE n1.typeEvt = n2.typeEvt 
                    AND n1.nom = n2.nom AND id(n1) < id(n2)
            RETURN count(*) = 0 AS bool
            """
        msg = self.msg.format(regle)
        records, summary, keys = self.driver.execute_query(req)
        self.assertTrue(records[0].data()['bool'],msg)

if __name__ == '__main__':
    unittest.main()
