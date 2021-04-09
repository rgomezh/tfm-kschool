import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import os

class Subscriptions(object):
    """
    This python class read the subscriptions dataset and:
        . Clean
        . Visualization
        . Preprocess train and test sets
    """
    
    def __init__(self, data_root, subscriptions_file='suscripciones.csv'):    
        self.data_root = data_root
        self.subscriptions_file = os.path.join(self.data_root, subscriptions_file)
        self.subscriptions = None
        self.mensual_subscriptions = None
        
    def set_data(self):
        self.subscriptions = pd.read_csv(self.subscriptions_file, parse_dates = ['fecha_creacion', 'fecha_modificacion', 'fecha_inicio', 'fecha_fin'], 
                                         dtype = {'id_producto' : 'object', 'id_suscripcion_original' : 'object', 'id_suscripcion' : 'object'})

    def get_data(self):
        return self.subscriptions
        
    def clean_data(self):

        # Remove inconsistent records
        self.subscriptions =  self.subscriptions[(self.subscriptions['fecha_fin'] >= self.subscriptions['fecha_inicio'])]
        # To Review records without id_product and referencia_producto. If we know the price we may save the records, otherwise we will have to remove them
#         sus.subscriptions[sus.subscriptions['periodicidad'] == 'Mensual']['referencia_producto'].value_counts()
#         sus.subscriptions[sus.subscriptions['referencia_producto'].isna()]
        
        
        # The upgrades are marked in the final subscription and we need mark the source subscription
        upgrades = self.subscriptions[self.subscriptions['transicion'] == 'upgrade'][['id_suscripcion', 'id_suscripcion_original']]
        upgrades.columns = ['id_suscripcion_final','id_suscripcion_origen']        
        self.subscriptions = self.subscriptions.merge(upgrades, left_on='id_suscripcion', right_on='id_suscripcion_origen', how='left')    
        del self.subscriptions['id_suscripcion_origen']
        del self.subscriptions['id_suscripcion_original'] 
        self.subscriptions['transicion'] = False
        self.subscriptions['transicion'] = self.subscriptions['id_suscripcion_final'].apply(lambda x: True if pd.notnull(x) else False)
        
    
    def extract_mensual_suscriptions(self):
#        self.mensual_subscriptions = self.subscriptions[self.subscriptions['periodicidad'] == 'Mensual'][['cod_local', 'fecha_inicio', 'fecha_fin']]
        self.mensual_subscriptions = self.subscriptions[self.subscriptions['periodicidad'] == 'Mensual'][['cod_local']]        
        return self.mensual_subscriptions
    
    
    def view_data(self):
        pass
    
#     def models(self):
#         pass
    
#     def metrics(self)
    
