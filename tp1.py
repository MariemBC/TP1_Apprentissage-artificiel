import numpy as np
import pandas as pd
import itertools

#1.Créer d'un DataFrame en utilisant les données de fichier
data = pd.read_table('market_basket.txt')

#2.Affichier 10 premiers ligne
print(data.iloc[1:11])

#3.Afficher les dimensions du dataframe.
print(data.shape)

#4.Écrire un script python qui permet de Construire un table binaire indiquant la présence de chaque produit au niveau 
# des caddies (True:1 si le produit est présent dans le caddie et 0 dans le cas réciproque).
col=data['Product'].sort_values().unique()
lig=data['ID'].unique()

matrix=np.zeros((len(lig),len(col)))
k=0
for i in lig:
  df=data[data["ID"]==i]
  a=0
  for j in col:
    if df['Product'].str.contains(j).any():
      matrix[k][a]=1
    a=a+1
  k=k+1

df = pd.DataFrame(matrix, index=lig,columns=col)
print(df)


# 5.Tester la bibliothèque pandas.crosstab pour construire la table binaire et vérifier que vous avez les mêmes 
# résultats de votre script.
df=pd.crosstab(data['ID'],data['Product'])
print(df)

#6.Afficher les 30 premières transactions et les 3 premiers produits.
print(df.iloc[:3,:30])

#7.Écrire un script python de la fonction a_priori() qui permet l’extraction des itemsets les plus fréquents. 
# ( on définit un min_supp=0.025 et un longueur maximum de 4 produits)

nbr_max_produit=2 
def ExtractItemset(df, n):
    return list(itertools.combinations(df, n))

def CalculSupport (df,subsets,n):
  tab=[]
  k=0
  for i in subsets:
    subset=df[list(i)]
    w=subset[subset.sum(axis='columns')==n].count()
    tab.append(w[0])
    k=k+1
  return(tab)
min_supp=0.025*len(lig)
for i in range(1,nbr_max_produit+1):
  itemset=ExtractItemset(col,i)
  Support=CalculSupport(df,itemset,i)
  ff= pd.DataFrame(itemset)
  sup=pd.DataFrame(Support)
  sup.columns=['Support']
  frame=[ff,sup]
  F=pd.concat(frame,axis=1)
  C=F[F["Support"]>min_supp]
  print("C",i)
  print(C)
  
def Regle(item):
  it=item[:-1]
  for i in range(1,nbr_max_produit):
    List=ExtractItemset(it,i)
    PremisList=List[:-i]
    CclList=List[i:]
    PremisSupport=CalculSupport(df,PremisList,i)
    TotalSupport=CalculSupport(df,[it],nbr_max_produit)
  return(PremisList,CclList,np.array(TotalSupport)/np.array(PremisSupport))

AprioriRes=[]
k=0
for i in C.index:
  k=k+1
  ligne=list(C.loc[i,:])
  Premis,Ccl,Confidence=Regle(ligne)
  print('Regle :',Premis,' -> ',Ccl,' With confidence',Confidence)


  from mlxtend.frequent_patterns import apriori, association_rules
frq_items = apriori(df, min_support = 0.025, use_colnames = True)
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

#8.Afficher les 15 premiers itemsets.
print(rules.iloc[1:30])

#9.Ecrire une fonction is_inclus() qui permet de vérifier si un sous-ensemble items est inclus dans l’ensemble x.
def is_inclus(_subset,_set):
  if len(_subset)>len(_set):
    return(False)
  for i in _subset:
    if not(i in _set):
      return(False)
  return(True)
print(is_inclus(['Mariem','Ben Chaalia'],['Mariem','Ben Chaalia','3IDL']))


#10.Afficher les itemsets comprenant le produit ‘Aspirin’.
Rules_itemset=[list(a)+list(c) for a,c in zip(rules['antecedents'],rules['consequents'])]
for i in Rules_itemset:
  if is_inclus(['Aspirin'],i):
    print(i)
    
    
     #11.Afficher les itemsets contenant Aspirin et Eggs.
for i in Rules_itemset:
  if is_inclus(['Aspirin','Eggs'],i):
    print(i)   
    
    
#12.Nous produisons les règles à partir des itemsets fréquents. Elles peuvent être très nombreuses,nous en limitons 
# la prolifération en définissant un seuil minimal (min_threshold = 0.75) sur une mesure d’intérêt, en l’occurrence 
# la confiance dans notre exemple (metric = ‘’confidence’’). 
rules = association_rules(frq_items, metric ="confidence", min_threshold = 0.75)
    


#13.Afficher les 5 premières règles.
print(rules[:5])

#14.Filtrer les règles en affichant celles qui présentent un LIFT supérieur ou égal à 7.
print(rules[rules.lift>7])

#15.Filtrer les règles en affichant celles menant au conséquent {‘2pct_milk’}.
print(rules[rules.consequents.str.contains('2pct_Milk', na=True)] )
