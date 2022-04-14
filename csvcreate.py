import pandas as pd


i = 1
while i <= 64:
    df = pd.DataFrame()
    df['integer'] = []
    df['Wallet Address'] = []
    df['Private key'] = []
    print(f"writing {i}")
    df.to_csv(f'wallet{i}.csv', mode='a', index=False, header=True)
    i += 1