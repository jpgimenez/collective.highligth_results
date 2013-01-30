#! /bin/sh

I18NDOMAIN="collective.highlighted_results"
I18NDUDE="i18ndude"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
$I18NDUDE rebuild-pot --pot locales/${I18NDOMAIN}.pot \
    --merge locales/manual.pot \
    --create ${I18NDOMAIN} \
    --exclude=static .

# Synchronise the resulting .pot with all .po files
for po in locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    $I18NDUDE sync --pot locales/${I18NDOMAIN}.pot $po
done
