class TestPhraseLength:

    def test_phrase_length(self):
        phrase = input("Введите фразу менее 15 символов: ")
        assert len(phrase)<15, f"Фраза '{phrase}' содержит больше 15 символов"