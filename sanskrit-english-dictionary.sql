CREATE TABLE IF NOT EXISTS "synonym" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"synonym" varchar(255) NOT NULL DEFAULT '100',
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "sanskrit_word" (
	"id" int NOT NULL DEFAULT '11',
	"TechnicalTermDevanagari" varchar(255) NOT NULL DEFAULT '100',
	"TechnicalTermRomanized" varchar(255) NOT NULL DEFAULT '100',
	"Etymology" varchar(255) DEFAULT '400',
	"Derivation" varchar(255) DEFAULT '400',
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "english_translation" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"translation" varchar(255) NOT NULL DEFAULT '255',
	"detailedExplanation" text,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "antonym" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"antonym" varchar(255) NOT NULL DEFAULT '100',
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "example" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"example_sentence" text,
	"applicabilityModernContext" text,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "ReferenceNyayaText" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"source" varchar(255) NOT NULL DEFAULT '100',
	"description" varchar(255) DEFAULT '400',
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "pictorialIllustrations" (
	"id" int NOT NULL DEFAULT '11',
	"sanskrit_word_id" int NOT NULL DEFAULT '11',
	"illustrationLink" text NOT NULL,
	"image" longblob,
	PRIMARY KEY ("id")
);

ALTER TABLE "synonym" ADD CONSTRAINT "synonym_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_word"("id");
ALTER TABLE "english_translation" ADD CONSTRAINT "english_translation_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_word"("id");
ALTER TABLE "antonym" ADD CONSTRAINT "antonym_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_words"("id");
ALTER TABLE "example" ADD CONSTRAINT "example_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_word"("id");
ALTER TABLE "ReferenceNyayaText" ADD CONSTRAINT "ReferenceNyayaText_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_word"("id,");
ALTER TABLE "pictorialIllustrations" ADD CONSTRAINT "pictorialIllustrations_fk1" FOREIGN KEY ("sanskrit_word_id") REFERENCES "sanskrit_word"("id");
