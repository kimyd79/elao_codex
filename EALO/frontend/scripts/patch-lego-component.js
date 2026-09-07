const fs = require('fs')
const path = require('path')

const tokenFile = path.join(
  __dirname,
  '..',
  'node_modules',
  'lego-component',
  'styles',
  'token',
  'lego',
  '_legoComponentTokens.scss'
)

if (!fs.existsSync(tokenFile)) {
  throw new Error(`lego-component token file not found: ${tokenFile}`)
}

const replacements = [
  [
    '$lego-form-box__h-divider: 0 solid $lego__border-color--default !default',
    '$lego-form-box__h-divider: 0 solid $lego__border-color--default !default;'
  ],
  [
    '$lego-form-row__v-divider: 0 solid $lego__border-color--default !default',
    '$lego-form-row__v-divider: 0 solid $lego__border-color--default !default;'
  ]
]

let contents = fs.readFileSync(tokenFile, 'utf8')
for (const [legacyLine, correctedLine] of replacements) {
  if (contents.includes(correctedLine)) continue
  if (!contents.includes(legacyLine)) {
    throw new Error(`Expected lego-component SCSS line was not found: ${legacyLine.trim()}`)
  }
  contents = contents.replace(legacyLine, correctedLine)
}

fs.writeFileSync(tokenFile, contents, 'utf8')
console.log('Applied the ELAO Dart Sass compatibility patch to lego-component 0.1.2.')
