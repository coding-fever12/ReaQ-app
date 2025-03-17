import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '../theme';

const PredictionCard = ({ prediction }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Prediction Result</Text>
      <Text style={styles.prediction}>{prediction}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
    borderRadius: 10,
    padding: 20,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 10,
  },
  prediction: {
    fontSize: 24,
    color: colors.primary,
    textAlign: 'center',
    fontWeight: 'bold',
  },
});

export default PredictionCard;