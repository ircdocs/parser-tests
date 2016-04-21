package main

// Written in 2016 by Daniel Oaks <daniel@danieloaks.net>
//
// To the extent possible under law, the author(s) have dedicated all copyright
// and related and neighboring rights to this software to the public domain
// worldwide. This software is distributed without any warranty.
//
// You should have received a copy of the CC0 Public Domain Dedication along
// with this software. If not, see
// <http://creativecommons.org/publicdomain/zero/1.0/>.

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"

	"gopkg.in/yaml.v2"

	"github.com/DanielOaks/girc-go/ircmsg"
	"github.com/docopt/docopt-go"
)

// MsgSplitTests holds the test cases for IRC message splitting
type MsgSplitTests struct {
	Tests []struct {
		Input string
		Atoms struct {
			Source *string
			Verb   string
			Params []string
			Tags   map[string]interface{}
		}
	}
}

func main() {
	version := "irc-parser-tests 0.1.0"
	usage := `irc-parser-tests Go script.
Usage:
	test.go run
	test.go -h | --help
	test.go --version
Options:
	-h --help          Show this screen.
	--version          Show version.`

	arguments, _ := docopt.Parse(usage, nil, true, version, false)

	if arguments["run"].(bool) {
		var passed int
		var failed int

		// msg-split tests
		fmt.Println("Running split tests")

		data, err := ioutil.ReadFile("tests/msg-split.yaml")
		if err != nil {
			log.Fatal("Could not open test file msg-split.yaml:", err.Error())
		}

		var msgSplitTests *MsgSplitTests

		err = yaml.Unmarshal(data, &msgSplitTests)
		if err != nil {
			log.Fatal("Could not unmarshal msg-split.yaml test file:", err.Error())
		}

		passed = 0
		failed = 0

		for _, test := range msgSplitTests.Tests {
			msg, err := ircmsg.ParseLine(test.Input)

			if err != nil {
				log.Fatal(
					"msg-parse: Test failed to parse: ",
					test.Input,
				)
			}

			if msg.Command != strings.ToUpper(test.Atoms.Verb) {
				fmt.Println(
					"msg.Command != test.Verb: expected",
					test.Atoms.Verb,
					"got",
					msg.Command,
				)
				failed++
				continue
			}

			if len(msg.Params) != len(test.Atoms.Params) {
				fmt.Println(
					"len(msg.Params) != len(test.Params): expected",
					len(test.Atoms.Params),
					"got",
					len(msg.Params),
				)
				failed++
				continue
			}

			for i, data := range test.Atoms.Params {
				if msg.Params[i] != data {
					fmt.Println(
						"msg.Params != test.Params: expected",
						test.Atoms.Params,
						"got",
						msg.Params,
					)
					failed++
					continue
				}
			}

			if test.Atoms.Source != nil && *test.Atoms.Source != msg.Prefix {
				fmt.Println(
					"msg.Prefix != test.Source: expected",
					*test.Atoms.Source,
					"got",
					msg.Prefix,
				)
				failed++
				continue
			}

			for name, value := range test.Atoms.Tags {
				tag, exists := msg.Tags[name]

				if !exists {
					fmt.Println(
						"Expected tag",
						name,
						"but does not exist",
					)
					failed++
					continue
				}

				if value == true {
					if tag.HasValue {
						fmt.Println(
							"Tag",
							name,
							"is not supposed to have value, but does!",
						)
						failed++
						continue
					}
				} else {
					if !tag.HasValue {
						fmt.Println(
							"Tag",
							name,
							"is supposed to have value, but doesn't!",
						)
						failed++
						continue
					}

					if tag.Value != value {
						fmt.Println(
							"Tag",
							name,
							"has wrong value. Expected",
							value,
							"got",
							tag.Value,
						)
						failed++
						continue
					}
				}
			}

			passed++
		}

		fmt.Println(" * Passed tests:", passed)
		fmt.Println(" * Failed tests:", failed)
	}
}
