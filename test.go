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

	"github.com/DanielOaks/girc-go/ircmatch"
	"github.com/DanielOaks/girc-go/ircmsg"
	"github.com/DanielOaks/girc-go/ircutils"
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

// MsgJoinTests holds the test cases for IRC message assembly
type MsgJoinTests struct {
	Tests []struct {
		Atoms struct {
			Source string
			Verb   string
			Params []string
			Tags   map[string]interface{}
		}
		Matches []string
	}
}

// MaskMatchTests holds the test cases for IRC mask matching.
type MaskMatchTests struct {
	Tests []struct {
		Mask    string
		Matches []string
		Fails   []string
	}
}

// MaskSplitTests holds the test cases for IRC userhost splitting.
type MaskSplitTests struct {
	Tests []struct {
		Source string
		Atoms  struct {
			Nick string
			User string
			Host string
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

		passed = 0
		failed = 0

		data, err := ioutil.ReadFile("tests/msg-split.yaml")
		if err != nil {
			log.Fatal("Could not open test file msg-split.yaml:", err.Error())
		}

		var msgSplitTests *MsgSplitTests

		err = yaml.Unmarshal(data, &msgSplitTests)
		if err != nil {
			log.Fatal("Could not unmarshal msg-split.yaml test file:", err.Error())
		}

		for _, test := range msgSplitTests.Tests {
			msg, err := ircmsg.ParseLine(test.Input)

			if err != nil {
				log.Fatal(
					"msg-split: Test failed to parse: ",
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

		// msg-join tests
		fmt.Println("Running join tests")

		passed = 0
		failed = 0

		data, err = ioutil.ReadFile("tests/msg-join.yaml")
		if err != nil {
			log.Fatal("Could not open test file msg-join.yaml:", err.Error())
		}

		var msgJoinTests *MsgJoinTests

		err = yaml.Unmarshal(data, &msgJoinTests)
		if err != nil {
			log.Fatal("Could not unmarshal msg-join.yaml test file:", err.Error())
		}

		for _, test := range msgJoinTests.Tests {
			var tags *map[string]ircmsg.TagValue
			if test.Atoms.Tags != nil {
				tagsDict := make(map[string]ircmsg.TagValue)
				for key, value := range test.Atoms.Tags {
					if value == true {
						tagsDict[key] = ircmsg.NoTagValue()
					} else {
						tagsDict[key] = ircmsg.MakeTagValue(value.(string))
					}
				}
				tags = &tagsDict
			}

			msg := ircmsg.MakeMessage(tags, test.Atoms.Source, test.Atoms.Verb, test.Atoms.Params...)
			line, err := msg.Line()

			if err != nil {
				log.Fatal(
					"msg-join: Test failed to parse: ",
					err.Error(),
				)
			}

			var hasPassed bool
			for _, test := range test.Matches {
				if strings.TrimRight(line, "\r\n") == test {
					hasPassed = true
				}
			}
			if hasPassed {
				passed++
			} else {
				failed++
			}
		}

		fmt.Println(" * Passed tests:", passed)
		fmt.Println(" * Failed tests:", failed)

		// mask matching tests
		fmt.Println("Running mask matching tests")

		passed = 0
		failed = 0

		data, err = ioutil.ReadFile("tests/mask-match.yaml")
		if err != nil {
			log.Fatal("Could not open test file mask-match.yaml:", err.Error())
		}

		var maskMatchTests *MaskMatchTests

		err = yaml.Unmarshal(data, &maskMatchTests)
		if err != nil {
			log.Fatal("Could not unmarshal mask-match.yaml test file:", err.Error())
		}

		for _, test := range maskMatchTests.Tests {
			mask := ircmatch.MakeMatch(test.Mask)

			var testfailed bool
			for _, matchString := range test.Matches {
				if !mask.Match(matchString) {
					fmt.Println(fmt.Sprintf("Expected mask [%s] to match input [%s] but it did not.", test.Mask, matchString))
					testfailed = true
				}
			}
			for _, matchString := range test.Fails {
				if mask.Match(matchString) {
					fmt.Println(fmt.Sprintf("Did not expect mask [%s] to match input [%s] but it did.", test.Mask, matchString))
					testfailed = true
				}
			}

			if testfailed {
				failed++
			} else {
				passed++
			}
		}

		fmt.Println(" * Passed tests:", passed)
		fmt.Println(" * Failed tests:", failed)

		// mask splitting tests
		fmt.Println("Running userhost splitting tests")

		passed = 0
		failed = 0

		data, err = ioutil.ReadFile("tests/userhost-split.yaml")
		if err != nil {
			log.Fatal("Could not open test file userhost-split.yaml:", err.Error())
		}

		var maskSplitTests *MaskSplitTests

		err = yaml.Unmarshal(data, &maskSplitTests)
		if err != nil {
			log.Fatal("Could not unmarshal userhost-split.yaml test file:", err.Error())
		}

		for _, test := range maskSplitTests.Tests {
			uh := ircutils.ParseUserhost(test.Source)

			var testfailed bool

			if uh.Nick != test.Atoms.Nick {
				fmt.Println(fmt.Sprintf("Expected nick from userhost [%s] to match test [%s] but it was [%s].", test.Source, test.Atoms.Nick, uh.Nick))
				testfailed = true
			}
			if uh.User != test.Atoms.User {
				fmt.Println(fmt.Sprintf("Expected user from userhost [%s] to match test [%s] but it was [%s].", test.Source, test.Atoms.User, uh.User))
				testfailed = true
			}
			if uh.Host != test.Atoms.Host {
				fmt.Println(fmt.Sprintf("Expected host from userhost [%s] to match test [%s] but it was [%s].", test.Source, test.Atoms.Host, uh.Host))
				testfailed = true
			}

			if testfailed {
				failed++
			} else {
				passed++
			}
		}

		fmt.Println(" * Passed tests:", passed)
		fmt.Println(" * Failed tests:", failed)
	}
}
