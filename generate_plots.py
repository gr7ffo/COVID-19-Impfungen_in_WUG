import pandas as pd
import plotly.express as px


# Get data from RKI Github
impfungen = pd.read_csv("Aktuell_Deutschland_Landkreise_COVID-19-Impfungen.csv", low_memory=False)
# https://datengui.de/statistik-erklaert/ags
ags = 9577  # NM: 9373, WUG: 9577
# Create dataframe
df = impfungen.loc[impfungen["LandkreisId_Impfort"] == ags].groupby(['Impfdatum', 'Impfschutz', 'Altersgruppe'], as_index=False).sum()
# Get latest datum
datum = df['Impfdatum'].values[-1]

# Stacked bars plot
fig = px.bar(df, x='Impfdatum', y='Anzahl', color='Altersgruppe',
             pattern_shape='Impfschutz', barmode='stack',
             pattern_shape_sequence=[".", "x", "+"])
fig.update_xaxes(range=['2022-02-01', datum])
fig.write_image('stacked-bars.png')

# Pie chart total numbers
day = df.where(df['Impfdatum'] == datum).dropna()
fig = px.pie(day, values='Anzahl', names='Altersgruppe')
fig.write_image('daily-numbers.png')

# Pie chart count of dose
fig = px.pie(day, values='Anzahl', names='Impfschutz')
fig.write_image('daily-counts.png')
