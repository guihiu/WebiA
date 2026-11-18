import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential



# configuração remove o limite do número máximo de colunas exibidas
pd.set_option('display.max_columns', None)


df = pd.read_csv('breast-cancer.csv')


# 2. Separação de features (X) e rótulo (y)
X = df.drop(columns=['id', 'diagnosis'])
y = (df['diagnosis'] == 'M').astype(int)  # 0 = Benigno, 1 = Maligno

y.value_counts()

# Percentual de banigno
print(f"{(y.value_counts()[0]/df.shape[0])*100}%")

# Percentual de maligno
print(f"{(y.value_counts()[1]/df.shape[0])*100}%")

# 3. Divisão em treino e teste (estratificada)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)



# 4. Padronização das variáveis
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# 5. Definição da arquitetura MLP

dense=Dense(16, activation='sigmoid')
net_model=Net()
vet={        Input(shape=(X_train_scaled.shape[1],)),  # 30 neurônios de entrada
        Dense(16, activation='sigmoid'),  # 1ª camada oculta
        Dropout(0.2),  # Regularização contra overfitting
        Dense(32, activation='sigmoid'),  # 2ª camada oculta
        Dropout(0.1),  # Regularização contra overfitting
        Dense(64, activation='sigmoid'),  # 3ª camada oculta
        Dropout(0.1),
        Dense(16, activation='sigmoid'),  # 3ª camada oculta
        Dropout(0.1),
        Dense(1, activation='relu'
        ),  # Saída binária (probabilidade de ser maligno)
        }
model = Sequential(
    [
vet
    ]
)




# 6. Compilação
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy'],
)



# 7. Treinamento
history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.2,  # 20% do treino usado para validação
    epochs=50,
    batch_size=16,
    verbose=1,
)

# 8. Avaliação no conjunto de teste
loss, accuracy = model.evaluate(X_test_scaled, y_test, verbose=0)
y_pred_prob = model.predict(X_test_scaled)
y_pred = (y_pred_prob >= 0.5).astype(int)

print(f'\nAcurácia no Teste: {accuracy * 100:.2f}%')
print(f'ROC-AUC Score: {roc_auc_score(y_test, y_pred_prob):.4f}')
print('\nMatriz de Confusão:')
print(confusion_matrix(y_test, y_pred))
print('\nRelatório de Métricas:')
print(
    classification_report(y_test, y_pred, target_names=['Benigno', 'Maligno'])
)


matriz_de_confusao = confusion_matrix(y_test, y_pred)
matriz_de_confusao



# Calculando a acurácia
print(f"{round((matriz_de_confusao[0][0] + matriz_de_confusao[1][1]) / y_test.count(), 4) * 100}%")



# Calculando a recall
print(f"{round(matriz_de_confusao[1][1] / (matriz_de_confusao[1][1] + matriz_de_confusao[1][0]), 4) * 100}%")


# Calculando a precisão
print(f"{round(matriz_de_confusao[1][1] / (matriz_de_confusao[1][1] + matriz_de_confusao[0][1]), 4) * 100}%")


recall   = matriz_de_confusao[1][1] / (matriz_de_confusao[1][1] + matriz_de_confusao[1][0])
precisao = matriz_de_confusao[1][1] / (matriz_de_confusao[1][1] + matriz_de_confusao[0][1])

f1 = 2 * ((precisao * recall) / (precisao + recall))
print(f"{round(f1 * 100, 4)}%")