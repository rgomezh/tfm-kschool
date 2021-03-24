import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import os
from sklearn.preprocessing import OneHotEncoder


class Users(object):
    """
    This python class read the users dataset and:
        . Clean
        . Visualization       
    """

    def __init__(self, data_root, users_file='dm_indicadores_usuario.csv'):    
        self.data_root = data_root
        self.users_file = os.path.join(self.data_root, users_file)
        self.users = None;        
        
    
    def set_data(self):
        self.users = pd.read_csv(self.users_file)

    def clean_data(self):
        self.users = self.users[~self.users['tipo_login'].isin(['trial','periodista'])]
        self.users.loc[:,'genero'] = self.users['genero'].apply(lambda x: 'u' if pd.isna(x) 
                                                          else 'm' if (x == 'masculino') 
                                                          else 'f' if (x == 'femenino') 
                                                          else x)
        self.users.reset_index(drop=True, inplace=True)
        del self.users['usuario'] 
        del self.users['cookie']         
        
        encoder = OneHotEncoder(handle_unknown='ignore')        
        for field in ['genero', 'tipo_login', 'tipo_navega', 'tipo_dispositivo']:
            fieldEncoded = encoder.fit_transform(self.users[field].values.reshape(-1,1))
            df_fieldEncoded = pd.DataFrame(fieldEncoded.todense(), columns=encoder.categories_[0])
            self.users = self.users.join(df_fieldEncoded)
            del self.users[field]  
                       
    
    def view_data(self):
        pass
    