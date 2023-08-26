# Objective:
#   Transform QIIME2 abundance file to format suitable for LefSe analysis

# 1 - Non-User
# 2 - User

import pandas as pd

import PyPluMA
import PyIO

class MetaPhlAn2LEfSePlugin:
    def input(self, inputfile):
        self.parameters = PyIO.readParameters(inputfile)
        self.abundance_file = PyPluMA.prefix()+"/"+self.parameters["abundance_file"]
        self.metadata_file = PyPluMA.prefix()+"/"+self.parameters["metadata_file"]

    def run(self):
        pass

    def output(self, outputfile):
        out_lefse = outputfile #"lefse_in.txt"
        metadata_df = pd.read_csv(self.metadata_file, sep="\t")
        #metadata_df["group"] = metadata_df["COCAINE USE"].apply(lambda x: 1 if x=="Non-User" else 2)
        metadata_df["group"] = metadata_df["fib4-label"]

        metadata_df["ClientID"] = metadata_df["CLIENT IDENTIFIER"]
        metadata_df = metadata_df[["group", "ClientID"]]

        df = pd.read_csv(self.abundance_file, index_col=0)
        #df = df.set_index(["Unnamed: 0"])

        # Normalize
        df = df.div(df.sum(axis=1), axis=0)

        df["ClientID"] = df.index
        # transform sample to match metadata
        df["ClientID"] = df["ClientID"].apply(lambda x: x.split("_")[0].replace(".", "/"))

        df = df.merge(metadata_df, how="left", on="ClientID")
        df.index = df["ClientID"]

        df_transposed = df.T

        df_transposed["bacteria"] = df_transposed.index

        df_transposed.to_csv(out_lefse, sep="\t")

