from keras.layers import Input, Concatenate, Embedding, LSTM, Dense, dot, Activation, concatenate, Lambda
from keras.models import Model
from keras.backend import argmax, cast
import numpy as np
from tqdm import tqdm


def build_discriminator(dimension, v_size):
    buggy_input_layer = Input(shape=(None,))
    fixed_input_layer = Input(shape=(None,))
    concatted = Concatenate()([buggy_input_layer, fixed_input_layer])
    embed_lay = Embedding(v_size, dimension, mask_zero=True)(concatted)
    x = LSTM(dimension)(embed_lay)
    out = Dense(1, activation='sigmoid')(x)
    disc = Model([buggy_input_layer, fixed_input_layer], out)
    disc.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'], loss_weights=[0.5])

    return disc


def build_generator(dimension, v_size, drop_prob):
    # Encoder
    buggy_input_layer = Input(shape=(None,))
    enc_embed_lay = Embedding(v_size, dimension, mask_zero=True)(buggy_input_layer)
    encoder_outputs, state_h, state_c = LSTM(dimension, return_sequences=True, return_state=True, dropout=drop_prob,
                                             recurrent_dropout=drop_prob)(enc_embed_lay)
    # Decoder
    fixed_input_layer = Input(shape=(None,))
    dec_embed_lay = Embedding(v_size, dimension, mask_zero=True)(fixed_input_layer)
    decoder_outputs = LSTM(dimension, return_sequences=True, dropout=drop_prob, recurrent_dropout=drop_prob)(
        dec_embed_lay, initial_state=[state_h, state_c])
    # Attention
    attention = dot([decoder_outputs, encoder_outputs], axes=[2, 2])
    attention = Activation('softmax', name='attention')(attention)
    context = dot([attention, encoder_outputs], axes=[2, 1])
    decoder_combined_context = concatenate([context, decoder_outputs])
    attention_context_output = Dense(dimension, activation="tanh")(decoder_combined_context)
    # Model output
    model_output = Dense(v_size, activation="softmax")(attention_context_output)
    # Build model
    gen = Model([buggy_input_layer, fixed_input_layer], model_output)

    return gen


def build_gan(gen, disc):
    disc.trainable = False
    buggy_input_layer = Input(shape=(None,))
    fixed_input_layer = Input(shape=(None,))
    gen_out = gen([buggy_input_layer, fixed_input_layer])
    argmax_layer = Lambda(lambda x: cast(argmax(x, axis=2), dtype='float32'))
    disc_out = disc([buggy_input_layer, argmax_layer(gen_out)])
    gan = Model([buggy_input_layer, fixed_input_layer], [disc_out, gen_out])
    # compile model
    gan.compile(loss=['binary_crossentropy', 'categorical_crossentropy'], optimizer='rmsprop', loss_weights=[1, 100])

    return gan


def build_enc_dec(dimension, cmv_size, cdv_size, drop_prob):
    # Encoder
    buggy_input_layer = Input(shape=(None,))
    enc_embed_lay = Embedding(cmv_size, dimension, mask_zero=True)(buggy_input_layer)
    encoder_outputs, state_h, state_c = LSTM(dimension, return_sequences=True, return_state=True, dropout=drop_prob, recurrent_dropout=drop_prob)(enc_embed_lay)
    # Decoder
    fixed_input_layer = Input(shape=(None,))
    dec_embed_lay = Embedding(cdv_size, dimension, mask_zero=True)(fixed_input_layer)
    decoder_outputs = LSTM(dimension, return_sequences=True, dropout=drop_prob, recurrent_dropout=drop_prob)(dec_embed_lay, initial_state=[state_h, state_c])
    # Attention
    attention = dot([decoder_outputs, encoder_outputs], axes=[2, 2])
    attention = Activation('softmax', name='attention')(attention)
    context = dot([attention, encoder_outputs], axes=[2, 1])
    decoder_combined_context = concatenate([context, decoder_outputs])
    attention_context_output = Dense(dimension, activation="tanh")(decoder_combined_context)
    # Model output
    model_output = Dense(cdv_size, activation="softmax")(attention_context_output)
    # Build model
    encoder_decoder = Model([buggy_input_layer, fixed_input_layer], model_output)
    encoder_decoder.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return encoder_decoder


def generate_fixed_ints_gan(gen, bugs, fixed_len, token_map, int_map, test=False, v_size=None):
    gntd_ints = np.zeros(shape=(len(bugs), fixed_len))
    gntd_ints[:, 0] = token_map["<sol>"]
    if test:
        test_predictions = np.zeros(shape=(len(bugs), fixed_len, v_size), dtype='float32')
        test_predictions[:, 0, token_map["<sol>"]] = 1.
    j = 0
    # Loop all training/testing set
    for buggy, generated in tqdm(zip(bugs, gntd_ints), total=len(bugs)):
        buggy_input = buggy[np.newaxis]
        gntd_in_out = generated[np.newaxis]
        # Loop 1 sequence
        for i in range(1, fixed_len):
            predictions = gen.predict([buggy_input, gntd_in_out])
            prediction = predictions.argmax(axis=2)[:, i]
            # print(predictions[:, i][0])
            # print(predictions[:, i][0].shape)
            if (not test) and int_map[prediction[0]] == "<eol>":
                break
            if test:
                test_predictions[j, i] = predictions[:, i]
            generated[i] = prediction
        j += 1
    if test:
        print('=============')
        print(test_predictions)
        print(test_predictions.shape)
        print(token_map["<sol>"])

        # if test:
        #     print(predictions.shape)
                # generated[i] = prediction[:, i]

    return gntd_ints if not test else test_predictions


def decode_ints_gan(int_matrix, int_map):
    gntd_codes = []
    for ints in int_matrix:
        # code = [int_map[x] for x in ints if x != 0]
        code = [int_map[x] for x in ints]
        truncated_code = []
        for token in code:
            if token != "<eol>":
                truncated_code.append(token)
            else:
                break
        # gntd_codes.append(truncated_code[1:])
        gntd_codes.append(truncated_code)

    return gntd_codes


def generate_fixed_ints_enc_dec(gen, bugs, fixed_len, token_map, int_map):
    gntd_ints = np.zeros(shape=(len(bugs), fixed_len))
    gntd_ints[:, 0] = token_map["<sol>"]
    for buggy, generated in tqdm(zip(bugs, gntd_ints), total=len(bugs)):
        buggy_input = buggy[np.newaxis]
        gntd_in_out = generated[np.newaxis]
        for i in range(1, fixed_len):
            prediction = gen.predict([buggy_input, gntd_in_out]).argmax(axis=2)
            generated[i] = prediction[:, i]
            if int_map[prediction[:, i][0]] == "<eol>":
                break

    return gntd_ints


def decode_ints_enc_dec(int_matrix, int_map):
    gntd_codes = []
    for ints in int_matrix:
        code = [int_map[x] for x in ints if x != 0]
        gntd_codes.append(code)

    return gntd_codes
