import React from 'react';
import { View, Image, StyleSheet, TouchableOpacity, Text } from 'react-native';
import * as ImagePicker from 'react-native-image-picker';
import { colors } from '../theme';

const CustomImagePicker = ({ onImageSelected, selectedImage }) => {
  const selectImage = () => {
    ImagePicker.launchImageLibrary(
      {
        mediaType: 'photo',
        includeBase64: true,
        maxHeight: 200,
        maxWidth: 200,
      },
      (response) => {
        if (response.didCancel) return;
        if (response.error) {
          console.error('ImagePicker Error: ', response.error);
          return;
        }
        onImageSelected(response);
      },
    );
  };

  return (
    <TouchableOpacity onPress={selectImage} style={styles.container}>
      {selectedImage ? (
        <Image source={{ uri: selectedImage.uri }} style={styles.image} />
      ) : (
        <View style={styles.placeholder}>
          <Text style={styles.placeholderText}>Tap to select image</Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: 200,
    borderRadius: 10,
    overflow: 'hidden',
    backgroundColor: colors.lightGray,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    color: colors.gray,
    fontSize: 16,
  },
});

export default CustomImagePicker;